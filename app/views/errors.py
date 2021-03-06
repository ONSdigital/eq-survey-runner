from flask import Blueprint, request, current_app, session as cookie_session
from flask_themes2 import render_theme_template
from flask_login import current_user
from flask_wtf.csrf import CSRFError
from sdc.crypto.exceptions import InvalidTokenException

from structlog import get_logger
from ua_parser import user_agent_parser

from app.authentication.no_token_exception import NoTokenException
from app.globals import get_metadata
from app.libs.utils import convert_tx_id_for_boxes
from app.submitter.submission_failed import SubmissionFailedException
from app.templating.template_renderer import TemplateRenderer

from app.utilities.cookies import analytics_allowed

logger = get_logger()

errors_blueprint = Blueprint('errors', __name__)


class MultipleSurveyError(Exception):
    pass


@errors_blueprint.app_errorhandler(401)
@errors_blueprint.app_errorhandler(NoTokenException)
def unauthorized(error=None):
    log_exception(error, 401)
    return render_template('session-expired.html'), 401


@errors_blueprint.app_errorhandler(CSRFError)
def csrf_error(error=None):
    metadata = get_metadata(current_user)
    if metadata and check_multiple_survey(metadata, request.view_args):
        log_exception(error, 200)
        return render_template('multiple_survey.html')

    log_exception(error, 401)
    return render_template('session-expired.html'), 401


@errors_blueprint.app_errorhandler(InvalidTokenException)
def forbidden(error=None):
    log_exception(error, 403)
    return _render_error_page(403)


@errors_blueprint.app_errorhandler(SubmissionFailedException)
def service_unavailable(error=None):
    log_exception(error, 503)
    return _render_error_page(503)


@errors_blueprint.app_errorhandler(MultipleSurveyError)
def multiple_survey_error(error=None):
    log_exception(error, 200)
    return render_template('multiple_survey.html')


@errors_blueprint.app_errorhandler(Exception)
def internal_server_error(error=None):
    log_exception(error, 500)
    return _render_error_page(500)


@errors_blueprint.app_errorhandler(403)
@errors_blueprint.app_errorhandler(404)
def http_exception(error):
    log_exception(error, error.code)
    return _render_error_page(error.code)


def log_exception(error, status_code):
    metadata = get_metadata(current_user)
    if metadata:
        logger.bind(tx_id=metadata['tx_id'])

    logger.error('an error has occurred', exc_info=error, url=request.url, status_code=status_code)


def _render_error_page(status_code):
    tx_id = get_tx_id()
    user_agent = user_agent_parser.Parse(request.headers.get('User-Agent', ''))

    cookie_message = request.cookies.get('ons_cookie_message_displayed')
    allow_analytics = analytics_allowed(request)
    return render_theme_template('default', 'errors/error.html',
                                 status_code=status_code,
                                 analytics_gtm_id=current_app.config['EQ_GTM_ID'],
                                 analytics_gtm_env_id=current_app.config['EQ_GTM_ENV_ID'],
                                 cookie_message=cookie_message,
                                 allow_analytics=allow_analytics,
                                 account_service_url=cookie_session.get('account_service_url'),
                                 ua=user_agent, tx_id=tx_id), status_code


def get_tx_id():
    tx_id = None
    metadata = get_metadata(current_user)
    if metadata:
        tx_id = convert_tx_id_for_boxes(metadata['tx_id'])
    return tx_id


def render_template(template_name):
    tx_id = get_tx_id()
    user_agent = user_agent_parser.Parse(request.headers.get('User-Agent', ''))

    cookie_message = request.cookies.get('ons_cookie_message_displayed')
    allow_analytics = analytics_allowed(request)
    return render_theme_template(cookie_session.get('theme', 'default'),
                                 template_name=template_name,
                                 analytics_gtm_id=current_app.config['EQ_GTM_ID'],
                                 analytics_gtm_env_id=current_app.config['EQ_GTM_ENV_ID'],
                                 cookie_message=cookie_message,
                                 allow_analytics=allow_analytics,
                                 ua=user_agent,
                                 tx_id=tx_id,
                                 account_service_url=cookie_session.get('account_service_url'),
                                 survey_title=TemplateRenderer.safe_content(cookie_session.get('survey_title', '')))


def check_multiple_survey(metadata, request_values):
    try:
        if metadata['eq_id'] != request_values['eq_id'] \
            or metadata['form_type'] != request_values['form_type'] \
                or metadata.get('collection_exercise_sid') != request_values.get('collection_id'):
            logger.bind(tx_id=metadata['tx_id'],
                        eq_id=request_values['eq_id'],
                        form_type=request_values['form_type'],
                        ce_id=request_values.get('collection_id'))

            return True
    except KeyError:
        return False
