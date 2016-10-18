import logging

from app.data_model.questionnaire_store import get_metadata
from app.libs.utils import convert_tx_id
from app.main.views.questionnaire import questionnaire_blueprint
from app.schema.exceptions import QuestionnaireException
from app.submitter.submission_failed import SubmissionFailedException

from flask import request
from flask.ext.themes2 import render_theme_template

from flask_login import current_user

from ua_parser import user_agent_parser

logger = logging.getLogger(__name__)


@questionnaire_blueprint.app_errorhandler(200)
def index(error=None):
    log_exception(error)
    return _render_error_page(200)


@questionnaire_blueprint.app_errorhandler(400)
def bad_request(error=None):
    log_exception(error)
    return _render_error_page(400)


@questionnaire_blueprint.app_errorhandler(401)
def unauthorized(error=None):
    log_exception(error)
    return _render_error_page(401)


@questionnaire_blueprint.app_errorhandler(403)
def forbidden(error=None):
    log_exception(error)
    return _render_error_page(403)


@questionnaire_blueprint.app_errorhandler(404)
@questionnaire_blueprint.app_errorhandler(QuestionnaireException)
def page_not_found(error=None):
    log_exception(error)
    return _render_error_page(404)


@questionnaire_blueprint.app_errorhandler(503)
@questionnaire_blueprint.app_errorhandler(SubmissionFailedException)
def service_unavailable(error=None):
    log_exception(error)
    return _render_error_page(503)


@questionnaire_blueprint.app_errorhandler(500)
@questionnaire_blueprint.app_errorhandler(Exception)
def internal_server_error(error=None):
    log_exception(error)
    return _render_error_page(500)


def log_exception(error):
    if error:
        logger.error(error)
        logger.exception(error)


def _render_error_page(status_code):
    tx_id = None
    metadata = get_metadata(current_user)
    if metadata:
        tx_id = convert_tx_id(metadata["tx_id"])
    user_agent = user_agent_parser.Parse(request.headers.get('User-Agent', ''))
    return render_theme_template('default', 'errors/error.html',
                                 status_code=status_code,
                                 ua=user_agent, tx_id=tx_id), status_code
