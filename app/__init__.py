import json
import logging
import os
import sys
from datetime import timedelta

from flask import Flask
from flask import url_for
from flask.ext.cache import Cache
from flask_babel import Babel
from flask_themes2 import Themes
from flaskext.markdown import Markdown
from structlog import get_logger

from app import settings
from app.authentication.authenticator import login_manager
from app.authentication.cookie_session import SHA256SecureCookieSessionInterface
from app.data_model.database import db_session
from app.libs.utils import get_locale
from app.submitter.submitter import SubmitterFactory

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


def rabbitmq_available():
    submitter = SubmitterFactory.get_submitter()
    if submitter.send_test():
        logger.info('rabbitmq healthtest ok')
        return True, "rabbit mq ok"
    else:
        logger.error('cannot connect to message server')
        return False, "rabbit mq unavailable"


def git_revision():
    return True, settings.EQ_GIT_REF


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

    configure_flask_logging(application)

    login_manager.init_app(application)

    if settings.EQ_ENABLE_CACHE:
        cache.init_app(application, config={'CACHE_TYPE': 'simple'})
    else:
        cache.init_app(application)  # Doesnt cache

    if settings.EQ_DEV_MODE:
        add_health_check(application, headers)
        start_dev_mode(application)

    # always add safe health check
    add_safe_health_check(application)

    if settings.EQ_PROFILING:
        setup_profiling(application)

    if settings.EQ_UA_ID:
        setup_analytics(application)

    if settings.EQ_GIT_REF:
        logger.info('starting eq survey runner', version=settings.EQ_GIT_REF)

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
    from flask_analytics import Analytics
    from app.analytics.custom_google_analytics import CustomGoogleAnalytics

    Analytics.provider_map['google_analytics'] = CustomGoogleAnalytics
    Analytics(application)
    application.config['ANALYTICS'][
        'GOOGLE_ANALYTICS']['ACCOUNT'] = settings.EQ_UA_ID


def configure_flask_logging(application):
    # set the logger for this application and stop using flasks broken solution
    application._logger = logging.getLogger(__name__)  # pylint: disable=protected-access
    # workaround flask crazy logging mechanism (https://github.com/pallets/flask/issues/641)
    application.logger_name = "nowhere"
    # the line below is required to trigger disabling the logger
    application.logger  # pylint: disable=pointless-statement


def start_dev_mode(application):
    # import and register the dev mode blueprint
    from app.views.dev_mode import dev_mode_blueprint
    application.register_blueprint(dev_mode_blueprint)
    application.debug = True
    # Not in dev mode, so use secure_session_cookies
    application.config['SESSION_COOKIE_SECURE'] = False

    if settings.EQ_ENABLE_FLASK_DEBUG_TOOLBAR:
        from flask_debugtoolbar import DebugToolbarExtension
        DebugToolbarExtension(application)
        application.config['DEBUG_TB_PROFILER_ENABLED'] = True
        application.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


def add_blueprints(application):
    # import and regsiter the main application blueprint
    from app.views.questionnaire import questionnaire_blueprint
    application.register_blueprint(questionnaire_blueprint)
    questionnaire_blueprint.config = application.config.copy()

    from app.views.session import session_blueprint
    application.register_blueprint(session_blueprint)
    session_blueprint.config = application.config.copy()

    from app.views.flush import flush_blueprint
    application.register_blueprint(flush_blueprint)
    flush_blueprint.config = application.config.copy()

    from app.views.errors import errors_blueprint
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
    from healthcheck import HealthCheck
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
