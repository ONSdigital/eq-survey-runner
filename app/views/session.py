from flask import Blueprint, current_app
from flask import redirect
from flask import request
from flask import session
from flask_login import current_user
from structlog import get_logger
from werkzeug.exceptions import NotFound, Unauthorized

from app.authentication.authenticator import store_session, decrypt_token
from app.authentication.jti_claim_storage import JtiTokenUsed, JtiClaimStorage
from app.globals import get_answer_store, get_completed_blocks
from app.questionnaire.path_finder import PathFinder
from app.storage.metadata_parser import parse_metadata
from app.utilities.schema import load_schema_from_metadata

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
    decrypted_token = decrypt_token(request.args.get('token'))
    metadata = parse_metadata(decrypted_token)
    eq_id = metadata["eq_id"]
    form_type = metadata["form_type"]
    tx_id = metadata["tx_id"]
    ru_ref = metadata["ru_ref"]
    logger.bind(eq_id=eq_id, form_type=form_type, tx_id=tx_id, ru_ref=ru_ref)
    logger.info("decrypted token and parsed metadata")

    if not eq_id or not form_type:
        logger.error("missing eq id or form type in jwt")
        raise NotFound

    # logging in again clears any session state
    if session:
        session.clear()

    jti_claim = metadata.get('jti')
    if jti_claim is None:
        logger.debug('jti claim not provided')
    else:
        try:
            jti_claim_storage = JtiClaimStorage(current_app.eq['database'])
            jti_claim_storage.use_jti_claim(jti_claim)
        except JtiTokenUsed as e:
            raise Unauthorized from e

    store_session(metadata)

    json = load_schema_from_metadata(metadata)

    navigator = PathFinder(json, get_answer_store(current_user), metadata)
    current_location = navigator.get_latest_location(get_completed_blocks(current_user))

    return redirect(current_location.url(metadata))
