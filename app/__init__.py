from flask import Flask
from flask.ext.babel import Babel
from flask.ext.login import LoginManager
from app.libs.utils import get_locale
from healthcheck import HealthCheck
from flaskext.markdown import Markdown
from app.utilities.factory import factory
from app.responses.response_store import FlaskResponseStore
from app.navigation.navigation_store import FlaskNavigationStore
from app.navigation.navigation_history import FlaskNavigationHistory
from app.validation.validation_store import FlaskValidationStore
from app import settings
from app.authentication.authenticator import Authenticator
from app.authentication.cookie_session import SHA256SecureCookieSessionInterface
from app.submitter.submitter import SubmitterFactory
from datetime import timedelta
import watchtower
import logging
from logging.handlers import RotatingFileHandler
import sys

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


def rabbitmq_available():
    submitter = SubmitterFactory.get_submitter()
    if submitter.send_test():
        logging.info('RabbitMQ Healthtest OK')
        return True, "rabbit mq ok"
    else:
        logging.error('Cannot connect to RabbbitMQ')
        return False, "rabbit mq unavailable"


def get_git_revision():
    git_revision = settings.EQ_GIT_REF
    return git_revision

GIT_REVISION = get_git_revision()


def git_revision():
    return True, GIT_REVISION

login_manager = LoginManager()


@login_manager.request_loader
def load_user(request):
    logging.debug("Calling load user")
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
    application.healthcheck = HealthCheck(application, '/healthcheck', success_headers=headers, failed_headers=headers)
    application.healthcheck.add_check(rabbitmq_available)
    application.healthcheck.add_check(git_revision)
    application.babel = Babel(application)
    application.babel.localeselector(get_locale)
    application.jinja_env.add_extension('jinja2.ext.i18n')

    application.secret_key = settings.EQ_SECRET_KEY
    application.permanent_session_lifetime = timedelta(seconds=settings.EQ_SESSION_TIMEOUT)

    application.wsgi_app = AWSReverseProxied(application.wsgi_app)

    application.session_interface = SHA256SecureCookieSessionInterface()

    Markdown(application, extensions=['gfm'])

    # import and regsiter the main application blueprint
    from .main import main_blueprint
    application.register_blueprint(main_blueprint)
    main_blueprint.config = application.config.copy()

    if settings.EQ_DEV_MODE:
        # import and register the pattern library blueprint
        from .patternlib import patternlib_blueprint
        application.register_blueprint(patternlib_blueprint)

        # import and register the dev mode blueprint
        from .dev_mode import dev_mode_blueprint
        application.register_blueprint(dev_mode_blueprint)
    else:
        # Not in dev mode, so use secure_session_cookies
        application.config['SESSION_COOKIE_SECURE'] = True

    from app.jinja_filters import blueprint as filter_blueprint
    application.register_blueprint(filter_blueprint)

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

    if settings.EQ_CLOUDWATCH_LOGGING:
        # filter out botocore messages, we don't wish to log these
        class NoBotocoreFilter(logging.Filter):
            def filter(self, record):
                return not record.name.startswith('botocore')

        log_group = settings.EQ_SR_LOG_GROUP
        cloud_watch_handler = watchtower.CloudWatchLogHandler(log_group=log_group)

        cloud_watch_handler.addFilter(NoBotocoreFilter())

        application.logger.addHandler(cloud_watch_handler)               # flask logger
        # we DO NOT WANT the root logger logging to cloudwatch as thsi causes weird recursion errors
        logging.getLogger().addHandler(cloud_watch_handler)      # root logger
        logging.getLogger(__name__).addHandler(cloud_watch_handler)      # module logger
        logging.getLogger('werkzeug').addHandler(cloud_watch_handler)    # werkzeug framework logger

    # setup file logging
    rotating_log_file = RotatingFileHandler(LOG_NAME, maxBytes=LOG_SIZE, backupCount=LOG_NUMBER)
    logging.getLogger().addHandler(rotating_log_file)

    application.logger.debug("Initializing login manager for application")
    login_manager.init_app(application)
    application.logger.debug("Login Manager initialized")

    # workaround flask crazy logging mechanism
    application.logger_name = "nowhere"
    application.logger

    # Setup profiling
    if settings.EQ_PROFILING:
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

    return application
