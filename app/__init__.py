from flask import Flask
from flask.ext.babel import Babel
from flask.ext.login import LoginManager
from app.libs.utils import get_locale
from healthcheck import HealthCheck, EnvironmentDump
from flaskext.markdown import Markdown
from app import settings
from app.authentication.authenticator import Authenticator
from app.submitter.submitter import Submitter
from datetime import timedelta
import pytz
import os.path
import newrelic.agent
import watchtower
import logging

newrelic_config = settings.EQ_NEW_RELIC_CONFIG_FILE
if os.path.isfile(newrelic_config):
    newrelic.agent.initialize(newrelic_config)


DISPLAY_DATETIME_FORMAT = '%A %d %B %Y at %H:%M'
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
EUROPE_LONDON = pytz.timezone("Europe/London")


def rabbitmq_available():
    submitter = Submitter()
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


def create_app(config_name):
    application = Flask(__name__, static_url_path='/s')
    headers = {'Content-Type': 'application/json', 'Cache-Control': 'no-cache, no-store, must-revalidate', 'Pragma': 'no-cache'}
    application.healthcheck = HealthCheck(application, '/healthcheck', success_headers=headers, failed_headers=headers)
    application.healthcheck.add_check(rabbitmq_available)
    application.healthcheck.add_check(git_revision)
    application.babel = Babel(application)
    application.babel.localeselector(get_locale)
    application.jinja_env.add_extension('jinja2.ext.i18n')
    application.envdump = EnvironmentDump(application, '/environment')

    application.secret_key = settings.EQ_SECRET_KEY
    application.permanent_session_lifetime = timedelta(seconds=settings.EQ_SESSION_TIMEOUT)

    Markdown(application, extensions=['gfm'])

    # import and regsiter the main application blueprint
    from .main import main_blueprint
    application.register_blueprint(main_blueprint)
    main_blueprint.config = application.config.copy()

    # import and register the pattern library blueprint
    from .patternlib import patternlib_blueprint
    application.register_blueprint(patternlib_blueprint)

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

    application.logger.debug("Initializing login manager for application")
    login_manager.init_app(application)
    application.logger.debug("Login Manager initialized")

    # workaround flask crazy logging mechanism
    application.logger_name = "nowhere"
    application.logger

    return application
