from datetime import datetime

from dateutil.tz import tzutc
from flask import Blueprint, redirect, request, g, session as cookie_session
from flask import url_for
from flask_login import logout_user
from marshmallow import ValidationError
from sdc.crypto.exceptions import InvalidTokenException
from structlog import get_logger
from werkzeug.exceptions import Unauthorized

from app.authentication.authenticator import store_session, decrypt_token
from app.authentication.jti_claim_storage import JtiTokenUsed, use_jti_claim
from app.globals import get_session_timeout_in_seconds
from app.helpers.template_helper import render_template
from app.storage.metadata_parser import (
    validate_questionnaire_claims,
    validate_runner_claims,
)
from app.utilities.schema import load_schema_from_metadata

logger = get_logger()

session_blueprint = Blueprint('session', __name__)


@session_blueprint.after_request
def add_cache_control(response):
    response.cache_control.no_cache = True
    return response


@session_blueprint.route('/session', methods=['HEAD'])
def login_head():
    return '', 204


@session_blueprint.route('/session', methods=['GET', 'POST'])
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

    try:
        runner_claims = validate_runner_claims(decrypted_token)
    except ValidationError as e:
        raise InvalidTokenException('Invalid runner claims') from e

    g.schema = load_schema_from_metadata(runner_claims)
    schema_metadata = g.schema.json['metadata']

    try:
        questionnaire_claims = validate_questionnaire_claims(
            decrypted_token, schema_metadata
        )
    except ValidationError as e:
        raise InvalidTokenException('Invalid questionnaire claims') from e

    claims = {**runner_claims, **questionnaire_claims}

    schema_name = claims['schema_name']
    tx_id = claims['tx_id']
    ru_ref = claims['ru_ref']
    questionnaire_id = claims['questionnaire_id']

    logger.bind(
        schema_name=schema_name,
        tx_id=tx_id,
        ru_ref=ru_ref,
        questionnaire_id=questionnaire_id,
    )
    logger.info('decrypted token and parsed metadata')

    store_session(claims)

    cookie_session['theme'] = g.schema.json['theme']
    cookie_session['survey_title'] = g.schema.json['title']
    cookie_session['expires_in'] = get_session_timeout_in_seconds(g.schema)

    if claims.get('account_service_url'):
        cookie_session['account_service_url'] = claims.get('account_service_url')

    if claims.get('account_service_log_out_url'):
        cookie_session['account_service_log_out_url'] = claims.get(
            'account_service_log_out_url'
        )

    return redirect(url_for('questionnaire.get_questionnaire'))


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


@session_blueprint.route('/session-expired', methods=['GET'])
def get_session_expired():
    logout_user()

    return render_template('errors/session-expired')


@session_blueprint.route('/signed-out', methods=['GET'])
def get_sign_out():
    """
    Signs the user first out of eq, then the account service by hitting the account services'
    logout url.
    """
    logout_user()

    account_service_log_out_url = cookie_session.get('account_service_log_out_url')
    if account_service_log_out_url:
        return redirect(account_service_log_out_url)

    return render_template(template='signed-out')
