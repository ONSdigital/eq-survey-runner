from flask import Flask
from flask import url_for
from flask_babel import Babel
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_session import SqlAlchemySessionInterface
from app.libs.utils import get_locale
from healthcheck import HealthCheck
from flaskext.markdown import Markdown
from app.utilities.factory import factory
from app.responses.response_store import FlaskResponseStore
from app.navigation.navigation_store import FlaskNavigationStore
from app.navigation.navigation_history import FlaskNavigationHistory
from app.validation.validation_store import FlaskValidationStore
from app.metadata.metadata_store import MetaDataStore
from app.authentication.authenticator import Authenticator
from app.authentication.cookie_session import SHA256SecureCookieSessionInterface
from app.submitter.submitter import SubmitterFactory
from app.utilities.strings import to_str
from app import settings
from datetime import timedelta
import watchtower
import logging
import sys
from logging.handlers import RotatingFileHandler
from flask_analytics import Analytics
from splunk_handler import SplunkHandler
from app.analytics.custom_google_analytics import CustomGoogleAnalytics


SECURE_HEADERS = {
    'Cache-Control': 'no-cache, no-store, must-revalidate',
    'Pragma': 'no-cache',
    'Strict-Transport-Security': 'max-age=31536000; includeSubdomains',
    'X-Frame-Options': 'DENY',
    'X-Xss-Protection': '1; mode=block',
    'X-Content-Type-Options': 'nosniff'
}

LOG_NAME = "eq.log"
LOG_SIZE = 1048576
LOG_NUMBER = 10

logger = logging.getLogger(__name__)


# setup the factory
logger.debug("Registering factory classes")
factory.register("response-store", FlaskResponseStore)
factory.register("navigation-store", FlaskNavigationStore)
factory.register("navigation-history", FlaskNavigationHistory)
factory.register("validation-store", FlaskValidationStore)
factory.register("metadata-store", MetaDataStore)


def rabbitmq_available():
    submitter = SubmitterFactory.get_submitter()
    if submitter.send_test():
        logging.info('RabbitMQ Healthtest OK')
        return True, "rabbit mq ok"
    else:
        logging.error('Cannot connect to Message Server')
        return False, "rabbit mq unavailable"


def get_git_revision():
    git_revision = settings.EQ_GIT_REF
    return git_revision

GIT_REVISION = get_git_revision()


def git_revision():
    return True, GIT_REVISION

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    logger.debug("Loading user %s", user_id)
    logger.debug(user_id)
    authenticator = Authenticator()
    return authenticator.check_session()


@login_manager.request_loader
def request_load_user(request):
    logger.debug("Load user %s", request)
    authenticator = Authenticator()
    return authenticator.check_session()


class AWSReverseProxied(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        scheme = environ.get('HTTP_X_FORWARDED_PROTO', 'http')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)


def create_app(config_name):
    application = Flask(__name__, static_url_path='/s')
    headers = {'Content-Type': 'application/json',
               'Cache-Control': 'no-cache, no-store, must-revalidate',
               'Pragma': 'no-cache',
               'Strict-Transport-Security': 'max-age=31536000; includeSubdomains',
               'X-Frame-Options': 'DENY',
               'X-Xss-Protection': '1; mode=block',
               'X-Content-Type-Options': 'nosniff'}

    db = setup_database(application)

    setup_babel(application)

    @application.after_request
    def apply_caching(response):
        for k, v in SECURE_HEADERS.items():
            response.headers[k] = v

        return response

    @application.context_processor
    def override_url_for():
        return dict(url_for=versioned_url_for)

    if settings.EQ_SERVER_SIDE_STORAGE:
        setup_server_side_database_sessions(application, db)
    else:
        setup_secure_cookies(application)

    application.wsgi_app = AWSReverseProxied(application.wsgi_app)

    Markdown(application, extensions=['gfm'])

    add_blueprints(application)

    configure_logging(application)

    if settings.EQ_DEV_MODE:
        # TODO fix health check so it no longer sends message to queue
        add_health_check(application, headers)
        start_dev_mode(application)

    if settings.EQ_PROFILING:
        setup_profiling(application)

    if settings.EQ_UA_ID:
        setup_analytics(application)

    return application


def setup_profiling(application):
    # Setup profiling

    from werkzeug.contrib.profiler import ProfilerMiddleware, MergeStream
    import os

    profiling_dir = "profiling"

    f = open('profiler.log', 'w')
    stream = MergeStream(sys.stdout, f)

    if not os.path.exists(profiling_dir):
        os.makedirs(profiling_dir)

    application.config['PROFILE'] = True
    application.wsgi_app = ProfilerMiddleware(application.wsgi_app, stream, profile_dir=profiling_dir)
    application.debug = True


def setup_analytics(application):
    # Setup analytics

    Analytics.provider_map['google_analytics'] = CustomGoogleAnalytics
    Analytics(application)
    application.config['ANALYTICS']['GOOGLE_ANALYTICS']['ACCOUNT'] = settings.EQ_UA_ID


def configure_logging(application):
    # set up some sane logging, as opposed to what flask does by default
    FORMAT = "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"
    levels = {
      'CRITICAL': logging.CRITICAL,
      'ERROR': logging.ERROR,
      'WARNING': logging.WARNING,
      'INFO': logging.INFO,
      'DEBUG': logging.DEBUG
    }
    logging.basicConfig(level=levels[settings.EQ_LOG_LEVEL], format=FORMAT)

    # set the logger for this application and stop using flasks broken solution
    application._logger = logging.getLogger(__name__)

    # turn boto logging to critical as it logs far too much and it's only used for cloudwatch logging
    logging.getLogger("botocore").setLevel(logging.ERROR)
    if settings.EQ_CLOUDWATCH_LOGGING:
        setup_cloud_watch_logging(application)

    # setup file logging
    rotating_log_file = RotatingFileHandler(LOG_NAME, maxBytes=LOG_SIZE, backupCount=LOG_NUMBER)
    logging.getLogger().addHandler(rotating_log_file)

    # setup splunk logging
    if settings.EQ_SPLUNK_LOGGING:
        setup_splunk_logging()
    application.logger.debug("Initializing login manager for application")
    login_manager.init_app(application)
    application.logger.debug("Login Manager initialized")

    # workaround flask crazy logging mechanism
    application.logger_name = "nowhere"
    application.logger


def setup_splunk_logging():
    splunk_handler = SplunkHandler(host=settings.EQ_SPLUNK_HOST,
                                   port=settings.EQ_SPLUNK_PORT,
                                   username=settings.EQ_SPLUNK_USERNAME,
                                   password=settings.EQ_SPLUNK_PASSWORD,
                                   index=settings.EQ_SPLUNK_INDEX,
                                   verify=False)
    logging.getLogger().addHandler(splunk_handler)


def setup_cloud_watch_logging(application):
    # filter out botocore messages, we don't wish to log these
    class NoBotocoreFilter(logging.Filter):
        def filter(self, record):
            return not record.name.startswith('botocore')

    log_group = settings.EQ_SR_LOG_GROUP
    cloud_watch_handler = watchtower.CloudWatchLogHandler(log_group=log_group)
    cloud_watch_handler.addFilter(NoBotocoreFilter())
    application.logger.addHandler(cloud_watch_handler)  # flask logger
    # we DO NOT WANT the root logger logging to cloudwatch as thsi causes weird recursion errors
    logging.getLogger().addHandler(cloud_watch_handler)  # root logger
    logging.getLogger(__name__).addHandler(cloud_watch_handler)  # module logger
    logging.getLogger('werkzeug').addHandler(cloud_watch_handler)  # werkzeug framework logger


def start_dev_mode(application):
    # import and register the pattern library blueprint
    from .patternlib import patternlib_blueprint
    application.register_blueprint(patternlib_blueprint)
    # import and register the dev mode blueprint
    from .dev_mode import dev_mode_blueprint
    application.register_blueprint(dev_mode_blueprint)
    application.debug = True
    # Not in dev mode, so use secure_session_cookies
    application.config['SESSION_COOKIE_SECURE'] = False


def add_blueprints(application):
    # import and regsiter the main application blueprint
    from .main import main_blueprint
    application.register_blueprint(main_blueprint)
    main_blueprint.config = application.config.copy()

    from app.jinja_filters import blueprint as filter_blueprint
    application.register_blueprint(filter_blueprint)


def setup_secure_cookies(application):
    application.secret_key = settings.EQ_SECRET_KEY
    application.permanent_session_lifetime = timedelta(seconds=settings.EQ_SESSION_TIMEOUT)
    application.session_interface = SHA256SecureCookieSessionInterface()
    application.config['SESSION_COOKIE_SECURE'] = True


def setup_babel(application):
    application.babel = Babel(application)
    application.babel.localeselector(get_locale)
    application.jinja_env.add_extension('jinja2.ext.i18n')


def add_health_check(application, headers):
    application.healthcheck = HealthCheck(application, '/healthcheck', success_headers=headers, failed_headers=headers)
    application.healthcheck.add_check(rabbitmq_available)
    application.healthcheck.add_check(git_revision)


def versioned_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            filename = get_minimized_asset(filename)
            # use the git revision
            version = settings.EQ_GIT_REF
            values['filename'] = filename
            values['q'] = version
    return url_for(endpoint, **values)


def get_minimized_asset(filename):
    '''
    If we're in production and it's a js or css file, return the minified version.
    :param filename: the original filename
    :return: the new file name will be .min.css or .min.js
    '''
    if settings.EQ_MINIMIZE_ASSETS:
        if 'css' in filename:
            filename = filename.replace(".css", ".min.css")
        elif 'js' in filename:
            filename = filename.replace(".js", ".min.js")
    return filename


def setup_database(application):
    application.config['SQLALCHEMY_DATABASE_URI'] = settings.EQ_SERVER_SIDE_STORAGE_DATABASE_URL
    db = SQLAlchemy(application)
    db.create_all()
    return db


def setup_server_side_database_sessions(application, db):
    application.permanent_session_lifetime = timedelta(seconds=settings.EQ_SESSION_TIMEOUT)
    application.secret_key = settings.EQ_SECRET_KEY
    application.config['SESSION_KEY_PREFIX'] = 'eq'
    application.config['SESSION_USE_SIGNER'] = True
    application.config['SESSION_COOKIE_SECURE'] = True
    application.session_cookie_name = "eq-session"

    # this is needed due to a bug in flask session
    class PrefixShim(object):
        def __add__(self, other):
            return "eq" + to_str(other)

    application.session_interface = SqlAlchemySessionInterface(application, db, "session", PrefixShim(), use_signer=True, permanent=True)
