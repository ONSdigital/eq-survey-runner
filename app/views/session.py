from flask import Blueprint, current_app, redirect, request, session
from flask_login import current_user, login_required
from flask_themes2 import render_theme_template

from werkzeug.exceptions import NotFound, Unauthorized

from structlog import get_logger

from app.authentication.authenticator import store_session, decrypt_token
from app.authentication.jti_claim_storage import JtiTokenUsed, JtiClaimStorage
from app.globals import get_answer_store, get_completed_blocks
from app.questionnaire.path_finder import PathFinder
from app.storage.metadata_parser import parse_metadata
from app.utilities.schema import load_schema_from_metadata
from app.helpers.session_helper import end_session_with_schema_context
from app.templating.template_renderer import TemplateRenderer

logger = get_logger()


session_blueprint = Blueprint('session', __name__)


@session_blueprint.after_request
def add_cache_control(response):
    response.cache_control.no_cache = True
    return response


@session_blueprint.route('/session', methods=['HEAD'])
def login_head():
    return '', 204


@session_blueprint.route('/session', methods=['GET'])
def login():
    """
    Initial url processing - expects a token parameter and then will authenticate this token. Once authenticated
    it will be placed in the users session
    :return: a 302 redirect to the next location for the user
    """
    # logging in again clears any session state
    if session:
        session.clear()

    decrypted_token = decrypt_token(request.args.get('token'))

    jti_claim = decrypted_token.get('jti')
    try:
        jti_claim_storage = JtiClaimStorage(current_app.eq['database'])
        jti_claim_storage.use_jti_claim(jti_claim)
    except JtiTokenUsed as e:
        raise Unauthorized from e

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

    store_session(metadata)

    json = load_schema_from_metadata(metadata)

    navigator = PathFinder(json, get_answer_store(current_user), metadata)
    current_location = navigator.get_latest_location(get_completed_blocks(current_user))

    return redirect(current_location.url(metadata))


@session_blueprint.route('/timeout-continue', methods=["GET"])
@login_required
def get_timeout_continue():
    return 'true'


@session_blueprint.route('/expire-session', methods=["POST"])
@login_required
def post_expire_session():
    end_session_with_schema_context()
    return get_session_expired()


@session_blueprint.route('/session-expired', methods=["GET"])
def get_session_expired():
    if current_user.is_active:
        end_session_with_schema_context()

    return render_theme_template(session['theme'], template_name='session-expired.html',
                                 analytics_ua_id=current_app.config['EQ_UA_ID'],
                                 survey_title=TemplateRenderer.safe_content(session['survey_title']))


@session_blueprint.route('/signed-out', methods=["GET"])
def get_sign_out():
    if current_user.is_active:
        end_session_with_schema_context()

    return render_theme_template(session['theme'], template_name='signed-out.html',
                                 analytics_ua_id=current_app.config['EQ_UA_ID'],
                                 survey_title=TemplateRenderer.safe_content(session['survey_title']))
