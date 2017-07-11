import json
import logging
import os
import sys
from datetime import timedelta
from uuid import uuid4

import yaml
from flask import Flask
from flask import url_for
from flask.ext.cache import Cache
from flask_babel import Babel
from flask_themes2 import Themes
from structlog import get_logger

from app import settings
from app.authentication.authenticator import login_manager
from app.authentication.cookie_session import SHA256SecureCookieSessionInterface

from app.authentication.session_storage import SessionStorage
from app.authentication.user_id_generator import UserIDGenerator
from app.data_model.database import Database

from app.new_relic import setup_newrelic
from app.secrets import SecretStore, validate_required_secrets

from app.submitter.submitter import LogSubmitter, RabbitMQSubmitter

SECURE_HEADERS = {
    'Cache-Control': 'no-cache, no-store, must-revalidate',
    'Pragma': 'no-cache',
    'Strict-Transport-Security': 'max-age=31536000; includeSubdomains',
    'X-Frame-Options': 'DENY',
    'X-Xss-Protection': '1; mode=block',
    'X-Content-Type-Options': 'nosniff',
}

cache = Cache()
logger = get_logger()


class AWSReverseProxied(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        scheme = environ.get('HTTP_X_FORWARDED_PROTO', 'http')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)


def create_app(setting_overrides=None):  # noqa: C901  pylint: disable=too-complex
    application = Flask(__name__, static_url_path='/s', static_folder='../static')
    application.config.from_object(settings)

    application.eq = {}

    secrets = yaml.safe_load(open(application.config['EQ_SECRETS_FILE']))
    validate_required_secrets(secrets)
    application.eq['secret_store'] = SecretStore(secrets)

    if setting_overrides:
        application.config.update(setting_overrides)

    if application.config['EQ_APPLICATION_VERSION']:
        logger.info('starting eq survey runner', version=application.config['EQ_APPLICATION_VERSION'])

    if application.config['EQ_NEW_RELIC_ENABLED']:
        setup_newrelic()

    if application.config['EQ_RABBITMQ_ENABLED']:
        application.eq['submitter'] = RabbitMQSubmitter(
            host=application.config['EQ_RABBITMQ_HOST'],
            secondary_host=application.config['EQ_RABBITMQ_HOST_SECONDARY'],
            port=application.config['EQ_RABBITMQ_PORT'],
            username=application.eq['secret_store'].get_secret_by_name('EQ_RABBITMQ_USERNAME'),
            password=application.eq['secret_store'].get_secret_by_name('EQ_RABBITMQ_PASSWORD'),
        )

    else:
        application.eq['submitter'] = LogSubmitter()

    application.eq['database'] = Database(
        driver=application.config['EQ_SERVER_SIDE_STORAGE_DATABASE_DRIVER'],
        host=application.config['EQ_SERVER_SIDE_STORAGE_DATABASE_HOST'],
        port=application.config['EQ_SERVER_SIDE_STORAGE_DATABASE_PORT'],
        database_name=application.config['EQ_SERVER_SIDE_STORAGE_DATABASE_NAME'],
        username=application.eq['secret_store'].get_secret_by_name('EQ_SERVER_SIDE_STORAGE_DATABASE_USERNAME'),
        password=application.eq['secret_store'].get_secret_by_name('EQ_SERVER_SIDE_STORAGE_DATABASE_PASSWORD'),
    )

    application.eq['session_storage'] = SessionStorage(
        application.eq['database'],
    )

    application.eq['id_generator'] = UserIDGenerator(
        application.config['EQ_SERVER_SIDE_STORAGE_USER_ID_ITERATIONS'],
        application.eq['secret_store'].get_secret_by_name('EQ_SERVER_SIDE_STORAGE_USER_ID_SALT'),
        application.eq['secret_store'].get_secret_by_name('EQ_SERVER_SIDE_STORAGE_USER_IK_SALT'),
    )

    setup_secure_cookies(application)

    setup_babel(application)

    application.wsgi_app = AWSReverseProxied(application.wsgi_app)

    add_blueprints(application)

    configure_flask_logging(application)

    login_manager.init_app(application)

    add_safe_health_check(application)

    if application.config['EQ_DEV_MODE']:
        start_dev_mode(application)

    if application.config['EQ_ENABLE_CACHE']:
        cache.init_app(application, config={'CACHE_TYPE': 'simple'})
    else:
        cache.init_app(application)  # Doesnt cache

    # Switch off flask default autoescaping as content is html encoded
    # during schema/metadata/summary context (and navigition) generation
    application.jinja_env.autoescape = False

    # Add theme manager
    application.config['THEME_PATHS'] = os.path.dirname(os.path.abspath(__file__))
    Themes(application, app_identifier="surveyrunner")

    @application.before_request
    def before_request():  # pylint: disable=unused-variable
        request_id = str(uuid4())
        logger.new(request_id=request_id)

    @application.after_request
    def apply_caching(response):  # pylint: disable=unused-variable
        for k, v in SECURE_HEADERS.items():
            response.headers[k] = v

        return response

    @application.context_processor
    def override_url_for():  # pylint: disable=unused-variable
        return dict(url_for=versioned_url_for)

    @application.teardown_appcontext
    def shutdown_session(exception=None):  # pylint: disable=unused-variable,unused-argument
        application.eq['database'].remove()

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


def configure_flask_logging(application):
    # set the logger for this application and stop using flasks broken solution
    application._logger = logging.getLogger(__name__)  # pylint: disable=protected-access
    # workaround flask crazy logging mechanism (https://github.com/pallets/flask/issues/641)
    application.logger_name = "nowhere"
    # the line below is required to trigger disabling the logger
    application.logger  # pylint: disable=pointless-statement


def start_dev_mode(application):
    # In dev mode, so don't use secure_session_cookies
    application.config['SESSION_COOKIE_SECURE'] = False

    if application.config['EQ_ENABLE_FLASK_DEBUG_TOOLBAR']:
        application.config['DEBUG_TB_PROFILER_ENABLED'] = True
        application.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
        application.debug = True
        from flask_debugtoolbar import DebugToolbarExtension
        DebugToolbarExtension(application)

    if application.config['EQ_PROFILING']:
        setup_profiling(application)


def add_blueprints(application):
    # import and register the main application blueprint
    from app.views.questionnaire import questionnaire_blueprint
    application.register_blueprint(questionnaire_blueprint)
    questionnaire_blueprint.config = application.config.copy()

    from app.views.session import session_blueprint
    application.register_blueprint(session_blueprint)
    session_blueprint.config = application.config.copy()

    from app.views.flush import flush_blueprint
    application.register_blueprint(flush_blueprint)
    flush_blueprint.config = application.config.copy()

    from app.views.dump import dump_blueprint
    application.register_blueprint(dump_blueprint)
    dump_blueprint.config = application.config.copy()

    from app.views.errors import errors_blueprint
    application.register_blueprint(errors_blueprint)
    errors_blueprint.config = application.config.copy()

    from app.jinja_filters import blueprint as filter_blueprint
    application.register_blueprint(filter_blueprint)


def setup_secure_cookies(application):
    session_timeout = application.config['EQ_SESSION_TIMEOUT_SECONDS']
    grace_period = application.config['EQ_SESSION_TIMEOUT_GRACE_PERIOD_SECONDS']
    application.secret_key = application.eq['secret_store'].get_secret_by_name('EQ_SECRET_KEY')
    application.permanent_session_lifetime = timedelta(seconds=session_timeout + grace_period)
    application.session_interface = SHA256SecureCookieSessionInterface()
    application.config['SESSION_COOKIE_SECURE'] = True


def setup_babel(application):
    application.babel = Babel(application)
    application.jinja_env.add_extension('jinja2.ext.i18n')


def add_safe_health_check(application):
    @application.route('/status')
    def safe_health_check():  # pylint: disable=unused-variable
        data = {
            'status': 'OK',
            'version': application.config['EQ_APPLICATION_VERSION'],
        }
        return json.dumps(data)


def versioned_url_for(endpoint, **values):

    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            filename = get_minimized_asset(filename)
            # use the git revision
            version = settings.EQ_APPLICATION_VERSION
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
