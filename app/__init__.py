from flask.ext.babel import Babel
import pytz
from flask import Flask
from app.libs.utils import get_locale
from healthcheck import HealthCheck, EnvironmentDump
from flaskext.markdown import Markdown

from app.submitter.submitter import Submitter

DISPLAY_DATETIME_FORMAT = '%A %d %B %Y at %H:%M'
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
EUROPE_LONDON = pytz.timezone("Europe/London")


def rabbitmq_available():
    submitter = Submitter()
    if submitter.send_test():
        return True, "rabbit mq ok"
    else:
        return False, "rabbit mq unavailable"


def create_app(config_name):
    application = Flask(__name__, static_url_path='/s')
    application.healthcheck = HealthCheck(application, '/healthcheck')
    application.healthcheck.add_check(rabbitmq_available)
    application.babel = Babel(application)
    application.babel.localeselector(get_locale)
    application.jinja_env.add_extension('jinja2.ext.i18n')
    application.envdump = EnvironmentDump(application, '/environment')
    application.markdown = Markdown(application, extensions=['gfm'])

    from .main import main as main_blueprint
    application.register_blueprint(main_blueprint)
    main_blueprint.config = application.config.copy()
    return application
