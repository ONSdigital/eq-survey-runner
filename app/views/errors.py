from flask import Blueprint
from flask import request
from flask.ext.themes2 import render_theme_template
from flask_login import current_user
from structlog import get_logger
from ua_parser import user_agent_parser

from app.authentication.flush_permission_denied import FlushPermissionDenied
from app.authentication.invalid_token_exception import InvalidTokenException
from app.authentication.no_survey_data_to_flush import NoSurveyDataToFlush
from app.authentication.no_token_exception import NoTokenException
from app.globals import get_metadata
from app.libs.utils import convert_tx_id
from app.schema.exceptions import QuestionnaireException
from app.submitter.submission_failed import SubmissionFailedException

logger = get_logger()

errors_blueprint = Blueprint('errors', __name__)


class MultipleSurveyError(Exception):
    pass


@errors_blueprint.after_request
def add_cache_control(response):
    response.cache_control.no_cache = True
    return response


@errors_blueprint.app_errorhandler(401)
@errors_blueprint.app_errorhandler(NoTokenException)
def unauthorized(error=None):
    log_exception(error)
    return _render_error_page(401)


@errors_blueprint.app_errorhandler(InvalidTokenException)
@errors_blueprint.app_errorhandler(FlushPermissionDenied)
def forbidden(error=None):
    log_exception(error)
    return _render_error_page(403)


@errors_blueprint.app_errorhandler(404)
@errors_blueprint.app_errorhandler(QuestionnaireException)
@errors_blueprint.app_errorhandler(NoSurveyDataToFlush)
def page_not_found(error=None):
    log_exception(error)
    return _render_error_page(404)


@errors_blueprint.app_errorhandler(SubmissionFailedException)
def service_unavailable(error=None):
    log_exception(error)
    return _render_error_page(503)


@errors_blueprint.app_errorhandler(MultipleSurveyError)
def multiple_survey_error(error=None):
    log_exception(error)
    return render_theme_template('default', 'multiple_survey.html')


@errors_blueprint.app_errorhandler(Exception)
def internal_server_error(error=None):
    log_exception(error)
    return _render_error_page(500)


def log_exception(error):
    if error:
        logger.error('an error has occurred', exc_info=error)
    else:
        logger.error('an error has occurred')


def _render_error_page(status_code):
    tx_id = get_tx_id()
    user_agent = user_agent_parser.Parse(request.headers.get('User-Agent', ''))
    return render_theme_template('default', 'errors/error.html',
                                 status_code=status_code,
                                 ua=user_agent, tx_id=tx_id), status_code


def get_tx_id():
    tx_id = None
    metadata = get_metadata(current_user)
    if metadata:
        tx_id = convert_tx_id(metadata["tx_id"])
    return tx_id
