from flask import Blueprint, request
from flask_login import current_user
from flask_wtf.csrf import CSRFError
from sdc.crypto.exceptions import InvalidTokenException
from structlog import get_logger

from app.authentication.no_token_exception import NoTokenException
from app.globals import get_metadata
from app.helpers.language_helper import handle_language
from app.helpers.template_helper import render_template
from app.submitter.submission_failed import SubmissionFailedException

logger = get_logger()

errors_blueprint = Blueprint('errors', __name__)


def log_error(error, status_code):
    metadata = get_metadata(current_user)
    if metadata:
        logger.bind(tx_id=metadata['tx_id'])

    log = logger.warning if status_code < 500 else logger.error

    log(
        'an error has occurred',
        exc_info=error,
        url=request.url,
        status_code=status_code,
    )


def _render_error_page(status_code, template=None):
    handle_language()
    template = template or status_code
    using_edge = request.user_agent.browser == 'edge'

    return (
        render_template(template=f'errors/{template}', using_edge=using_edge),
        status_code,
    )


@errors_blueprint.app_errorhandler(401)
@errors_blueprint.app_errorhandler(CSRFError)
@errors_blueprint.app_errorhandler(NoTokenException)
def unauthorized(error=None):
    log_error(error, 401)
    return _render_error_page(401, 'session-expired')


@errors_blueprint.app_errorhandler(InvalidTokenException)
def forbidden(error=None):
    log_error(error, 403)
    return _render_error_page(403)


@errors_blueprint.app_errorhandler(SubmissionFailedException)
@errors_blueprint.app_errorhandler(Exception)
def internal_server_error(error=None):
    try:
        log_error(error, 500)
        return _render_error_page(500)
    except Exception:  # pylint:disable=broad-except
        logger.error(
            'an error has occurred when rendering 500 error',
            exc_info=True,
            url=request.url,
            status_code=500,
        )
        return render_template(template='errors/500'), 500


@errors_blueprint.app_errorhandler(403)
@errors_blueprint.app_errorhandler(404)
def http_exception(error):
    log_error(error, error.code)
    return _render_error_page(error.code)
