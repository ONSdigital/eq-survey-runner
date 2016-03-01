from flask.ext.babel import Babel
from flask import Flask
from app.libs.utils import get_locale
from healthcheck import HealthCheck, EnvironmentDump
from flaskext.markdown import Markdown
from app import settings
from app.submitter.submitter import Submitter
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
    Markdown(application, extensions=['gfm'])

    from .main import main_blueprint
    application.register_blueprint(main_blueprint)
    main_blueprint.config = application.config.copy()
    return application
