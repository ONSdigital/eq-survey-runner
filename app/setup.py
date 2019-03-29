import copy
import json
import logging
import os
import sys
from datetime import timedelta
from uuid import uuid4

import boto3
import redis
import sqlalchemy
import yaml
from botocore.config import Config
from flask import Flask, url_for, session as cookie_session
from flask_babel import Babel
from flask_caching import Cache
from flask_talisman import Talisman
from flask_themes2 import Themes
from flask_wtf.csrf import CSRFProtect
from google.auth import credentials
from google.cloud import datastore
from sdc.crypto.key_store import KeyStore, validate_required_keys
from structlog import get_logger

from app import flask_theme_cache
from app import settings
from app.authentication.authenticator import login_manager
from app.authentication.cookie_session import SHA256SecureCookieSessionInterface
from app.authentication.user_id_generator import UserIDGenerator
from app.data_model.models import EQSession, QuestionnaireState, db
from app.globals import get_session_store
from app.keys import KEY_PURPOSE_SUBMISSION
from app.new_relic import setup_newrelic
from app.secrets import SecretStore, validate_required_secrets
from app.storage.datastore import DatastoreStorage
from app.storage.dynamodb import DynamodbStorage
from app.storage.redis import RedisStorage
from app.storage.sql import SqlStorage
from app.submitter.submitter import LogSubmitter, RabbitMQSubmitter, GCSSubmitter

CACHE_HEADERS = {
    'Cache-Control': 'no-cache, no-store, must-revalidate',
    'Pragma': 'no-cache',
}

CSP_POLICY = {
    'default-src': ["'self'", 'https://cdn.ons.gov.uk'],
    'font-src': ["'self'", 'data:', 'https://cdn.ons.gov.uk'],
    'script-src': ["'self'", 'https://www.google-analytics.com', 'https://cdn.ons.gov.uk'],
    'connect-src': ["'self'", 'https://www.google-analytics.com', 'https://cdn.ons.gov.uk'],
    'img-src': ["'self'", 'data:', 'https://www.google-analytics.com', 'https://cdn.ons.gov.uk'],
}

cache = Cache()

logger = get_logger()


class EmulatorCredentials(credentials.Credentials):
    """A mock GCP credential object.
    Used in conjunction with local emulators that don't require proper
    credentials e.g. Datastore
    """

    def __init__(self):  # pylint: disable=super-init-not-called
        self.token = b'seekrit'
        self.expiry = None

    @property
    def valid(self):
        return True

    def refresh(self, request):  # pylint: disable=unused-argument
        raise RuntimeError('Should never be refreshed.')


class AWSReverseProxied:

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

    with open(application.config['EQ_SECRETS_FILE']) as secrets_file:
        secrets = yaml.safe_load(secrets_file)

    with open(application.config['EQ_KEYS_FILE']) as keys_file:
        keys = yaml.safe_load(keys_file)

    validate_required_secrets(secrets)
    validate_required_keys(keys, KEY_PURPOSE_SUBMISSION)
    application.eq['secret_store'] = SecretStore(secrets)
    application.eq['key_store'] = KeyStore(keys)

    if setting_overrides:
        application.config.update(setting_overrides)

    if application.config['EQ_APPLICATION_VERSION']:
        logger.info('starting eq survey runner', version=application.config['EQ_APPLICATION_VERSION'])

    if application.config['EQ_NEW_RELIC_ENABLED']:
        setup_newrelic()

    setup_storage(application)

    setup_submitter(application)

    application.eq['id_generator'] = UserIDGenerator(
        application.config['EQ_SERVER_SIDE_STORAGE_USER_ID_ITERATIONS'],
        application.eq['secret_store'].get_secret_by_name('EQ_SERVER_SIDE_STORAGE_USER_ID_SALT'),
        application.eq['secret_store'].get_secret_by_name('EQ_SERVER_SIDE_STORAGE_USER_IK_SALT'),
    )

    setup_secure_cookies(application)

    setup_secure_headers(application)

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
        # no cache and silence warning
        cache.init_app(application, config={'CACHE_NO_NULL_WARNING': True})

    # Switch off flask default autoescaping as content is html encoded
    # during schema/metadata/summary context (and navigition) generation
    application.jinja_env.autoescape = False

    # Add theme manager
    application.config['THEME_PATHS'] = os.path.dirname(os.path.abspath(__file__))
    Themes(application, app_identifier='surveyrunner')

    # pylint: disable=no-member
    application.jinja_env.globals['theme'] = flask_theme_cache.get_global_theme_template(cache)

    @application.before_request
    def before_request():  # pylint: disable=unused-variable

        # While True the session lives for permanent_session_lifetime seconds
        # Needed to be able to set the client-side cookie expiration
        cookie_session.permanent = True

        request_id = str(uuid4())
        logger.new(request_id=request_id)

    @application.after_request
    def apply_caching(response):  # pylint: disable=unused-variable
        if 'text/html' in response.content_type:
            for k, v in CACHE_HEADERS.items():
                response.headers[k] = v
        else:
            response.headers['Cache-Control'] = 'max-age=2628000, public'

        return response

    @application.context_processor
    def override_url_for():  # pylint: disable=unused-variable
        return dict(url_for=versioned_url_for)

    return application


def setup_secure_headers(application):
    csp_policy = copy.deepcopy(CSP_POLICY)

    if application.config['EQ_ENABLE_LIVE_RELOAD']:
        # browsersync is configured to bind on port 5075
        csp_policy['connect-src'] += ['http://localhost:5075', 'ws://localhost:5075']

    Talisman(
        application,
        content_security_policy=csp_policy,
        content_security_policy_nonce_in=['script-src'],
        session_cookie_secure=application.config['EQ_ENABLE_SECURE_SESSION_COOKIE'],
        force_https=False,  # this is handled at the firewall
        strict_transport_security=True,
        strict_transport_security_max_age=31536000,
        frame_options='DENY')


def setup_storage(application):
    if application.config['EQ_STORAGE_BACKEND'] == 'datastore':
        setup_datastore(application)
    elif application.config['EQ_STORAGE_BACKEND'] == 'dynamodb':
        setup_dynamodb(application)
    elif application.config['EQ_STORAGE_BACKEND'] == 'sql':
        setup_database(application)
    else:
        raise Exception('Unknown EQ_STORAGE_BACKEND')

    setup_redis(application)


def get_database_uri(application):
    """ Returns database URI. Prefer SQLALCHEMY_DATABASE_URI over components."""
    if application.config.get('SQLALCHEMY_DATABASE_URI'):
        return application.config['SQLALCHEMY_DATABASE_URI']

    return '{driver}://{username}:{password}@{host}:{port}/{name}'\
           .format(driver=application.config['EQ_SERVER_SIDE_STORAGE_DATABASE_DRIVER'],
                   username=application.eq['secret_store'].get_secret_by_name('EQ_SERVER_SIDE_STORAGE_DATABASE_USERNAME'),
                   password=application.eq['secret_store'].get_secret_by_name('EQ_SERVER_SIDE_STORAGE_DATABASE_PASSWORD'),
                   host=application.config['EQ_SERVER_SIDE_STORAGE_DATABASE_HOST'],
                   port=application.config['EQ_SERVER_SIDE_STORAGE_DATABASE_PORT'],
                   name=application.config['EQ_SERVER_SIDE_STORAGE_DATABASE_NAME'])


def setup_database(application):
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    application.config['SQLALCHEMY_POOL_RECYCLE'] = 60
    application.config['SQLALCHEMY_DATABASE_URI'] = get_database_uri(application)

    with application.app_context():
        db.init_app(application)
        db.create_all()
        check_database()

    application.eq['storage'] = SqlStorage()


def check_database():
    md = sqlalchemy.MetaData()
    table = sqlalchemy.Table(QuestionnaireState.__tablename__,
                             md,
                             autoload=True,
                             autoload_with=db.engine)

    if 'version' not in table.c:  # pragma: no cover
        raise Exception('Database patch "pr-1347-apply.sql" has not been run')

    session_table = sqlalchemy.Table(EQSession.__tablename__,
                                     md,
                                     autoload=True,
                                     autoload_with=db.engine)

    if 'session_data' not in session_table.c:  # pragma: no cover
        raise Exception('Database patch "pr-1391-apply.sql" has not been run')

    if 'expires_at' not in session_table.c:  # pragma: no cover
        raise Exception('Database patch "pr-1797-apply.sql" has not been run')


def setup_dynamodb(application):
    # Number of additional connection attempts
    config = Config(
        retries={'max_attempts': application.config['EQ_DYNAMODB_MAX_RETRIES']},
        max_pool_connections=application.config['EQ_DYNAMODB_MAX_POOL_CONNECTIONS'],
    )

    dynamodb = boto3.resource('dynamodb', endpoint_url=application.config['EQ_DYNAMODB_ENDPOINT'], config=config)
    application.eq['storage'] = DynamodbStorage(dynamodb)


def setup_datastore(application):
    creds = EmulatorCredentials() if application.config['EQ_DATASTORE_EMULATOR_CREDENTIALS'] else None
    client = datastore.Client(_use_grpc=False, credentials=creds)
    application.eq['storage'] = DatastoreStorage(client)


def setup_redis(application):
    redis_client = redis.Redis(
        host=application.config['EQ_REDIS_HOST'],
        port=application.config['EQ_REDIS_PORT'],
    )

    application.eq['ephemeral_storage'] = RedisStorage(redis_client)


def setup_submitter(application):
    if application.config['EQ_SUBMISSION_BACKEND'] == 'gcs':
        bucket_id = application.config.get('EQ_GCS_SUBMISSION_BUCKET_ID')

        if not bucket_id:
            raise Exception('Setting EQ_GCS_SUBMISSION_BUCKET_ID Missing')

        application.eq['submitter'] = GCSSubmitter(bucket_name=bucket_id)

    elif application.config['EQ_SUBMISSION_BACKEND'] == 'rabbitmq':
        host = application.config.get('EQ_RABBITMQ_HOST')
        secondary_host = application.config.get('EQ_RABBITMQ_HOST_SECONDARY')

        if not host:
            raise Exception('Setting EQ_RABBITMQ_HOST Missing')
        if not secondary_host:
            raise Exception('Setting EQ_RABBITMQ_HOST_SECONDARY Missing')

        application.eq['submitter'] = RabbitMQSubmitter(
            host=host,
            secondary_host=secondary_host,
            port=application.config['EQ_RABBITMQ_PORT'],
            queue=application.config['EQ_RABBITMQ_QUEUE_NAME'],
            username=application.eq['secret_store'].get_secret_by_name('EQ_RABBITMQ_USERNAME'),
            password=application.eq['secret_store'].get_secret_by_name('EQ_RABBITMQ_PASSWORD'),
        )

    elif application.config['EQ_SUBMISSION_BACKEND'] == 'log':
        application.eq['submitter'] = LogSubmitter()

    else:
        raise Exception('Unknown EQ_SUBMISSION_BACKEND')


def setup_profiling(application):
    # Setup profiling

    from werkzeug.contrib.profiler import ProfilerMiddleware, MergeStream

    profiling_dir = 'profiling'

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
    application.logger_name = 'nowhere'
    # the line below is required to trigger disabling the logger
    application.logger  # pylint: disable=pointless-statement


def start_dev_mode(application):
    if application.config['EQ_ENABLE_FLASK_DEBUG_TOOLBAR']:
        application.config['DEBUG_TB_PROFILER_ENABLED'] = True
        application.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
        application.debug = True
        from flask_debugtoolbar import DebugToolbarExtension
        DebugToolbarExtension(application)

    if application.config['EQ_PROFILING']:
        setup_profiling(application)


def add_blueprints(application):
    csrf = CSRFProtect(application)

    # import and register the main application blueprint
    from app.views.questionnaire import questionnaire_blueprint
    application.register_blueprint(questionnaire_blueprint)
    questionnaire_blueprint.config = application.config.copy()

    from app.views.questionnaire import post_submission_blueprint
    application.register_blueprint(post_submission_blueprint)
    post_submission_blueprint.config = application.config.copy()

    from app.views.feedback import feedback_blueprint
    application.register_blueprint(feedback_blueprint)
    feedback_blueprint.config = application.config.copy()

    from app.views.session import session_blueprint
    csrf.exempt(session_blueprint)
    application.register_blueprint(session_blueprint)
    session_blueprint.config = application.config.copy()

    from app.views.flush import flush_blueprint
    csrf.exempt(flush_blueprint)
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

    from app.views.static import contact_blueprint
    application.register_blueprint(contact_blueprint)
    contact_blueprint.config = application.config.copy()

    from app.views.schema import schema_blueprint
    application.register_blueprint(schema_blueprint)
    schema_blueprint.config = application.config.copy()


def setup_secure_cookies(application):
    session_timeout = application.config['EQ_SESSION_TIMEOUT_SECONDS']
    application.secret_key = application.eq['secret_store'].get_secret_by_name('EQ_SECRET_KEY')
    application.permanent_session_lifetime = timedelta(seconds=session_timeout)
    application.session_interface = SHA256SecureCookieSessionInterface()


def setup_babel(application):
    application.babel = Babel(application)
    application.jinja_env.add_extension('jinja2.ext.i18n')

    @application.babel.localeselector
    def get_locale():  # pylint: disable=unused-variable
        session = get_session_store()

        if session and session.session_data:
            return session.session_data.language_code

        return None

    @application.babel.timezoneselector
    def get_timezone():  # pylint: disable=unused-variable
        # For now regardless of locale we will show times in GMT/BST
        return 'Europe/London'


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
            filename = filename.replace('.css', '.min.css')
        elif 'js' in filename:
            filename = filename.replace('.js', '.min.js')
    return filename
