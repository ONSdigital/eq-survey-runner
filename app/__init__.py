import json
import logging
import os
import sys
from datetime import timedelta

from logging.handlers import RotatingFileHandler

from app import settings
from app.analytics.custom_google_analytics import CustomGoogleAnalytics
from app.authentication.authenticator import Authenticator
from app.authentication.cookie_session import SHA256SecureCookieSessionInterface
from app.data_model.database import db_session
from app.libs.utils import get_locale
from app.submitter.submitter import SubmitterFactory

from flask import Flask
from flask import url_for

from flask_analytics import Analytics

from flask_babel import Babel

from flask_login import LoginManager

from flask_themes2 import Themes

from flaskext.markdown import Markdown

from healthcheck import HealthCheck

from splunk_handler import SplunkHandler

import watchtower

SECURE_HEADERS = {
    'Cache-Control': 'no-cache, no-store, must-revalidate',
    'Pragma': 'no-cache',
    'Strict-Transport-Security': 'max-age=31536000; includeSubdomains',
    'X-Frame-Options': 'DENY',
    'X-Xss-Protection': '1; mode=block',
    'X-Content-Type-Options': 'nosniff',
}

LOG_NAME = "eq.log"
LOG_SIZE = 1048576
LOG_NUMBER = 10

logger = logging.getLogger(__name__)


def rabbitmq_available():
    submitter = SubmitterFactory.get_submitter()
    if submitter.send_test():
        logging.info('RabbitMQ Healthtest OK')
        return True, "rabbit mq ok"
    else:
        logging.error('Cannot connect to Message Server')
        return False, "rabbit mq unavailable"


def git_revision():
    return True, settings.EQ_GIT_REF


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


def create_app():
    application = Flask(__name__, static_url_path='/s', static_folder='../static')
    headers = {'Content-Type': 'application/json',
               'Cache-Control': 'no-cache, no-store, must-revalidate',
               'Pragma': 'no-cache',
               'Strict-Transport-Security': 'max-age=31536000; includeSubdomains',
               'X-Frame-Options': 'DENY',
               'X-Xss-Protection': '1; mode=block',
               'X-Content-Type-Options': 'nosniff'}

    restrict_content_length(application)

    setup_secure_cookies(application)

    setup_babel(application)

    @application.after_request
    def apply_caching(response):  # pylint: disable=unused-variable
        for k, v in SECURE_HEADERS.items():
            response.headers[k] = v

        return response

    @application.context_processor
    def override_url_for():  # pylint: disable=unused-variable
        return dict(url_for=versioned_url_for)

    application.wsgi_app = AWSReverseProxied(application.wsgi_app)

    Markdown(application, extensions=['gfm'])

    add_blueprints(application)

    configure_logging(application)

    login_manager.init_app(application)

    if settings.EQ_DEV_MODE:
        # TODO fix health check so it no longer sends message to queue
        add_health_check(application, headers)
        start_dev_mode(application)

    # always add safe health check
    add_safe_health_check(application)

    if settings.EQ_PROFILING:
        setup_profiling(application)

    if settings.EQ_UA_ID:
        setup_analytics(application)

    # Add theme manager
    application.config['THEME_PATHS'] = os.path.dirname(os.path.abspath(__file__))
    Themes(application, app_identifier="surveyrunner")

    @application.teardown_appcontext
    def shutdown_session(exception=None):  # pylint: disable=unused-variable,unused-argument
        db_session.remove()

    return application


def setup_profiling(application):
    # Setup profiling

    from werkzeug.contrib.profiler import ProfilerMiddleware, MergeStream

    profiling_dir = "profiling"

    f = open('profiler.log', 'w')
    stream = MergeStream(sys.stdout, f)

    if not os.path.exists(profiling_dir):
        os.makedirs(profiling_dir)

    application.config['PROFILE'] = True
    application.wsgi_app = ProfilerMiddleware(
        application.wsgi_app, stream, profile_dir=profiling_dir)
    application.debug = True


def setup_analytics(application):
    # Setup analytics

    Analytics.provider_map['google_analytics'] = CustomGoogleAnalytics
    Analytics(application)
    application.config['ANALYTICS'][
        'GOOGLE_ANALYTICS']['ACCOUNT'] = settings.EQ_UA_ID


def configure_logging(application):
    # set up some sane logging, as opposed to what flask does by default
    log_format = "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"
    levels = {
        'CRITICAL': logging.CRITICAL,
        'ERROR': logging.ERROR,
        'WARNING': logging.WARNING,
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG,
    }
    logging.basicConfig(level=levels[settings.EQ_LOG_LEVEL], format=log_format)

    # set the logger for this application and stop using flasks broken solution
    application._logger = logging.getLogger(__name__)  # pylint: disable=protected-access

    # turn boto logging to critical as it logs far too much and it's only used
    # for cloudwatch logging
    logging.getLogger("botocore").setLevel(logging.ERROR)
    if settings.EQ_CLOUDWATCH_LOGGING:
        setup_cloud_watch_logging(application)

    # Set werkzeug logging level
    if settings.EQ_WERKZEUG_LOG_LEVEL:
        werkzeug_logger = logging.getLogger('werkzeug')
        werkzeug_logger.setLevel(level=levels[settings.EQ_WERKZEUG_LOG_LEVEL])

    # setup file logging
    rotating_log_file = RotatingFileHandler(
        LOG_NAME, maxBytes=LOG_SIZE, backupCount=LOG_NUMBER)
    logging.getLogger().addHandler(rotating_log_file)

    # setup splunk logging
    if settings.EQ_SPLUNK_LOGGING:
        setup_splunk_logging()

    # workaround flask crazy logging mechanism (https://github.com/pallets/flask/issues/641)
    application.logger_name = "nowhere"
    # the line below is required to trigger disabling the logger
    application.logger  # pylint: disable=pointless-statement


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
    # we DO NOT WANT the root logger logging to cloudwatch as thsi causes
    # weird recursion errors
    logging.getLogger().addHandler(cloud_watch_handler)  # root logger
    logging.getLogger(__name__).addHandler(cloud_watch_handler)  # module logger
    logging.getLogger('werkzeug').addHandler(
        cloud_watch_handler)  # werkzeug framework logger


def start_dev_mode(application):
    # import and register the dev mode blueprint
    from .dev_mode.views import dev_mode_blueprint
    application.register_blueprint(dev_mode_blueprint)
    application.debug = True
    # Not in dev mode, so use secure_session_cookies
    application.config['SESSION_COOKIE_SECURE'] = False


def add_blueprints(application):
    # import and regsiter the main application blueprint
    from .main.views.questionnaire import questionnaire_blueprint
    application.register_blueprint(questionnaire_blueprint)
    questionnaire_blueprint.config = application.config.copy()

    from .main.views.root import root_blueprint
    application.register_blueprint(root_blueprint)
    root_blueprint.config = application.config.copy()

    from .main.views.errors import errors_blueprint
    application.register_blueprint(errors_blueprint)
    errors_blueprint.config = application.config.copy()

    from app.jinja_filters import blueprint as filter_blueprint
    application.register_blueprint(filter_blueprint)


def setup_secure_cookies(application):
    application.secret_key = settings.EQ_SECRET_KEY
    application.permanent_session_lifetime = timedelta(
        seconds=settings.EQ_SESSION_TIMEOUT)
    application.session_interface = SHA256SecureCookieSessionInterface()
    application.config['SESSION_COOKIE_SECURE'] = True


def setup_babel(application):
    application.babel = Babel(application)
    application.babel.localeselector(get_locale)
    application.jinja_env.add_extension('jinja2.ext.i18n')


def add_health_check(application, headers):
    application.healthcheck = HealthCheck(
        application, '/healthcheck', success_headers=headers, failed_headers=headers)
    application.healthcheck.add_check(rabbitmq_available)
    application.healthcheck.add_check(git_revision)


def add_safe_health_check(application):
    @application.route('/status')
    def safe_health_check():  # pylint: disable=unused-variable
        data = {'status': 'OK'}
        return json.dumps(data)


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
    """
    If we're in production and it's a js or css file, return the minified version.
    :param filename: the original filename
    :return: the new file name will be .min.css or .min.js
    """
    if settings.EQ_MINIMIZE_ASSETS:
        if 'css' in filename:
            filename = filename.replace(".css", ".min.css")
        elif 'js' in filename:
            filename = filename.replace(".js", ".min.js")
    return filename


def restrict_content_length(application):
    application.config['MAX_CONTENT_LENGTH'] = settings.EQ_MAX_HTTP_POST_CONTENT_LENGTH
