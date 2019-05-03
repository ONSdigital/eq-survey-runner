from quart import Blueprint, request, current_app, render_template as render_quart_template, session as cookie_session

from flask_login import current_user
from flask_wtf.csrf import CSRFError
from sdc.crypto.exceptions import InvalidTokenException

from structlog import get_logger
from ua_parser import user_agent_parser

from app.authentication.no_token_exception import NoTokenException
from app.globals import get_metadata_async
from app.helpers.template_helper import safe_content
from app.libs.utils import convert_tx_id_for_boxes
from app.submitter.submission_failed import SubmissionFailedException

logger = get_logger()

errors_blueprint = Blueprint('errors', __name__)


@errors_blueprint.app_errorhandler(401)
@errors_blueprint.app_errorhandler(NoTokenException)
async def unauthorized(error=None):
    await log_exception(error, 401)
    return render_template('session-expired.html'), 401


@errors_blueprint.app_errorhandler(CSRFError)
async def csrf_error(error=None):
    await log_exception(error, 401)
    return render_template('session-expired.html'), 401


@errors_blueprint.app_errorhandler(InvalidTokenException)
async def forbidden(error=None):
    await log_exception(error, 403)
    return _render_error_page(403)


@errors_blueprint.app_errorhandler(SubmissionFailedException)
async def service_unavailable(error=None):
    await log_exception(error, 503)
    return _render_error_page(503)


@errors_blueprint.app_errorhandler(Exception)
async def internal_server_error(error=None):
    await log_exception(error, 500)
    return _render_error_page(500)


@errors_blueprint.app_errorhandler(403)
@errors_blueprint.app_errorhandler(404)
async def http_exception(error):
    await log_exception(error, error.code)
    return _render_error_page(error.code)


async def log_exception(error, status_code):
    metadata = await get_metadata_async(current_user)
    if metadata:
        logger.bind(tx_id=metadata['tx_id'])

    logger.error('an error has occurred', exc_info=error, url=request.url, status_code=status_code)


async def _render_error_page(status_code):
    tx_id = await get_tx_id()
    user_agent = user_agent_parser.Parse(request.headers.get('User-Agent', ''))

    return await render_quart_template('errors/error.html',
                                       status_code=status_code,
                                       analytics_ua_id=current_app.config['EQ_UA_ID'],
                                       account_service_url=cookie_session.get('account_service_url'),
                                       ua=user_agent, tx_id=tx_id), status_code


async def get_tx_id():
    tx_id = None
    metadata = await get_metadata_async(current_user)
    if metadata:
        tx_id = convert_tx_id_for_boxes(metadata['tx_id'])
    return tx_id


async def render_template(template_name):
    tx_id = await get_tx_id()
    user_agent = user_agent_parser.Parse(request.headers.get('User-Agent', ''))

    return await render_quart_template(template_name,
                                       analytics_ua_id=current_app.config['EQ_UA_ID'],
                                       ua=user_agent,
                                       tx_id=tx_id,
                                       account_service_url=cookie_session.get('account_service_url'),
                                       survey_title=safe_content(cookie_session.get('survey_title', '')))
