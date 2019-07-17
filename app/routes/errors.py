from flask import Blueprint, request
from flask_login import current_user
from flask_wtf.csrf import CSRFError
from sdc.crypto.exceptions import InvalidTokenException
from structlog import get_logger
from ua_parser import user_agent_parser

from app.authentication.no_token_exception import NoTokenException
from app.globals import get_metadata
from app.helpers.template_helper import render_template
from app.libs.utils import convert_tx_id_for_boxes
from app.submitter.submission_failed import SubmissionFailedException


logger = get_logger()

errors_blueprint = Blueprint('errors', __name__)


@errors_blueprint.app_errorhandler(401)
@errors_blueprint.app_errorhandler(NoTokenException)
def unauthorized(error=None):
    log_exception(error, 401)
    return _render_error_page(401, 'session-expired')


@errors_blueprint.app_errorhandler(CSRFError)
def csrf_error(error=None):
    log_exception(error, 401)
    return _render_error_page(401, 'session-expired')


@errors_blueprint.app_errorhandler(InvalidTokenException)
def forbidden(error=None):
    log_exception(error, 403)
    return _render_error_page(403)


@errors_blueprint.app_errorhandler(SubmissionFailedException)
def service_unavailable(error=None):
    log_exception(error, 503)
    return _render_error_page(503)


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

    logger.error(
        'an error has occurred',
        exc_info=error,
        url=request.url,
        status_code=status_code,
    )


def _render_error_page(status_code, template=None):
    tx_id = get_tx_id()
    user_agent = user_agent_parser.Parse(request.headers.get('User-Agent', ''))
    template = template or 'error'

    return (
        render_template(
            template=template, status_code=status_code, ua=user_agent, tx_id=tx_id
        ),
        status_code,
    )


def get_tx_id():
    tx_id = None
    metadata = get_metadata(current_user)
    if metadata:
        tx_id = convert_tx_id_for_boxes(metadata['tx_id'])
    return tx_id
