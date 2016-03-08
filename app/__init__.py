from flask import Flask
from flask.ext.babel import Babel
from flask.ext.login import LoginManager
from app.libs.utils import get_locale
from healthcheck import HealthCheck, EnvironmentDump
from flaskext.markdown import Markdown
from app import settings
from app.authentication.authenticator import Authenticator
from app.submitter.submitter import Submitter
from app.main.views.questionnaire_view import QuestionnaireView
from app.main.views.login_view import LoginView
from datetime import timedelta
import pytz
import os.path
import newrelic.agent
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
login_manager.session_protection = 'strong'


@login_manager.request_loader
def load_user(request):
    logging.debug("Calling load user %s")
    authenticator = Authenticator()
    return authenticator.check_session(request)


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

    application.logger.debug("Initializing login manager for application")
    login_manager.init_app(application)
    application.logger.debug("Login Manager initialized")

    # workaround flask crazy logging mechanism
    application.logger_name = "nowhere"
    application.logger

    add_views(application)

    return application


def add_views(application):
    application.add_url_rule('/questionnaire/<questionnaire_id>', view_func=QuestionnaireView.as_view("questionnaire"), methods=['GET', 'POST'])
    application.add_url_rule('/session', view_func=LoginView.as_view("login"), methods=['GET'])
