from flask import Blueprint
from flask import redirect
from flask import request
from flask import session
from flask_login import current_user
from structlog import get_logger
from werkzeug.exceptions import NotFound

from app.authentication import authenticator
from app.globals import get_answer_store, get_completed_blocks, get_metadata
from app.questionnaire.path_finder import PathFinder
from app.utilities.schema import get_schema

logger = get_logger()


session_blueprint = Blueprint('session', __name__)


@session_blueprint.after_request
def add_cache_control(response):
    response.cache_control.no_cache = True
    return response


@session_blueprint.route('/session', methods=['GET'])
def login():
    """
    Initial url processing - expects a token parameter and then will authenticate this token. Once authenticated
    it will be placed in the users session
    :return: a 302 redirect to the next location for the user
    """
    logger.new()
    # logging in again clears any session state
    if session:
        session.clear()

    logger.debug("attempting token authentication")
    authenticator.jwt_login(request)
    logger.debug("token authenticated - linking to session")

    metadata = get_metadata(current_user)

    eq_id = metadata["eq_id"]
    form_type = metadata["form_type"]

    logger.bind(eq_id=eq_id, form_type=form_type)

    if not eq_id or not form_type:
        logger.error("missing eq id or form type in jwt")
        raise NotFound

    json, _ = get_schema(metadata)

    navigator = PathFinder(json, get_answer_store(current_user), metadata)
    current_location = navigator.get_latest_location(get_completed_blocks(current_user))

    return redirect(current_location.url(metadata))
