from datetime import datetime

from dateutil.tz import tzutc
from flask import Blueprint, redirect, request, g, session as cookie_session
from flask_login import current_user, login_required, logout_user
from sdc.crypto.exceptions import InvalidTokenException

from werkzeug.exceptions import Unauthorized

from structlog import get_logger

from app.authentication.authenticator import store_session, decrypt_token
from app.authentication.jti_claim_storage import JtiTokenUsed, use_jti_claim
from app.globals import get_completeness
from app.settings import ACCOUNT_URL
from app.storage.metadata_parser import validate_metadata, parse_runner_claims
from app.utilities.schema import load_schema_from_metadata
from app.views.errors import render_template

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
    if cookie_session:
        cookie_session.clear()

    decrypted_token = decrypt_token(request.args.get('token'))
    validate_jti(decrypted_token)

    claims = parse_runner_claims(decrypted_token)

    g.schema = load_schema_from_metadata(claims)
    schema_metadata = g.schema.json['metadata']
    validate_metadata(claims, schema_metadata)

    eq_id = claims['eq_id']
    form_type = claims['form_type']
    tx_id = claims['tx_id']
    ru_ref = claims['ru_ref']

    logger.bind(eq_id=eq_id, form_type=form_type, tx_id=tx_id, ru_ref=ru_ref)
    logger.info('decrypted token and parsed metadata')

    store_session(claims)

    cookie_session['theme'] = g.schema.json['theme']
    cookie_session['survey_title'] = g.schema.json['title']

    if 'account_service_url' in claims and claims.get('account_service_url'):
        cookie_session[ACCOUNT_URL] = claims.get('account_service_url')

    current_location = get_completeness(current_user).get_latest_location()

    return redirect(current_location.url(claims))


def validate_jti(decrypted_token):
    expires = datetime.utcfromtimestamp(decrypted_token['exp']).replace(tzinfo=tzutc())
    if expires < datetime.now(tz=tzutc()):
        raise Unauthorized

    jti_claim = decrypted_token.get('jti')
    try:
        use_jti_claim(jti_claim, expires)
    except JtiTokenUsed as e:
        raise Unauthorized from e
    except (TypeError, ValueError) as e:
        raise InvalidTokenException from e


@session_blueprint.route('/timeout-continue', methods=['GET'])
@login_required
def get_timeout_continue():
    return 'true'


@session_blueprint.route('/expire-session', methods=['POST'])
@login_required
def post_expire_session():
    logout_user()
    return get_session_expired()


@session_blueprint.route('/session-expired', methods=['GET'])
def get_session_expired():

    logout_user()

    return render_template('session-expired.html')


@session_blueprint.route('/signed-out', methods=['GET'])
def get_sign_out():
    logout_user()

    return render_template('signed-out.html')
