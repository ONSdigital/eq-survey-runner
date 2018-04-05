from uuid import uuid4

from blinker import ANY
from flask import session as cookie_session, current_app
from flask_login import LoginManager, user_logged_out
from sdc.crypto.decrypter import decrypt
from sdc.crypto.exceptions import InvalidTokenException
from structlog import get_logger

from app.authentication.no_token_exception import NoTokenException
from app.authentication.user import User
from app.data_model.session_data import SessionData
from app.globals import get_questionnaire_store, get_session_store, create_session_store
from app.keys import KEY_PURPOSE_AUTHENTICATION

from app.settings import EQ_SESSION_ID, USER_IK


logger = get_logger()

login_manager = LoginManager()


@login_manager.user_loader
def user_loader(user_id):
    logger.debug('loading user', user_id=user_id)
    return load_user()


@login_manager.request_loader
def request_load_user(request):  # pylint: disable=unused-argument
    logger.debug('load user')
    return load_user()


@user_logged_out.connect_via(ANY)
def when_user_logged_out(sender_app, user):  # pylint: disable=unused-argument
    logger.debug('log out user')
    session_store = get_session_store()
    if session_store:
        session_store.delete()
    cookie_session.pop(USER_IK, None)


def load_user():
    """
    Checks for the present of the JWT in the users sessions
    :return: A user object if a JWT token is available in the session
    """
    session_store = get_session_store()
    if session_store and session_store.user_id:
        logger.debug('session exists')
        user_id = session_store.user_id
        user_ik = cookie_session.get(USER_IK)
        user = User(user_id, user_ik)

        if session_store.session_data.tx_id:
            logger.bind(tx_id=session_store.session_data.tx_id)

        return user

    else:
        logger.info('session does not exist')
        return None


def _create_session_data_from_metadata(metadata):
    """
    Creates a SessionData object from metadata
    :param metadata: metadata parsed from jwt token
    """
    session_data = SessionData(
        tx_id=metadata.get('tx_id'),
        eq_id=metadata.get('eq_id'),
        form_type=metadata.get('form_type'),
        period_str=metadata.get('period_str'),
        language_code=metadata.get('language_code'),
        survey_url=metadata.get('survey_url'),
        ru_name=metadata.get('ru_name'),
        ru_ref=metadata.get('ru_ref'),
        case_id=metadata.get('case_id'),
        case_ref=metadata.get('case_ref'),
        account_service_url=metadata.get('account_service_url')
    )
    return session_data


def store_session(metadata):
    """
    Store new session and metadata
    :param metadata: metadata parsed from jwt token
    """

    # also clear the secure cookie data
    cookie_session.clear()

    # get the hashed user id for eq
    id_generator = current_app.eq['id_generator']
    user_id = id_generator.generate_id(metadata)
    user_ik = id_generator.generate_ik(metadata)

    eq_session_id = str(uuid4())

    # store the user ik and es_session_id in the cookie
    cookie_session[USER_IK] = user_ik
    cookie_session[EQ_SESSION_ID] = eq_session_id

    session_data = _create_session_data_from_metadata(metadata)
    create_session_store(eq_session_id, user_id, user_ik, session_data)

    questionnaire_store = get_questionnaire_store(user_id, user_ik)
    questionnaire_store.metadata = metadata
    questionnaire_store.add_or_update()
    logger.info('user authenticated')


def decrypt_token(encrypted_token):
    logger.debug('decrypting token')
    if not encrypted_token or encrypted_token is None:
        raise NoTokenException('Please provide a token')

    mandatory_claims = ['eq_id', 'form_type', 'user_id', 'ru_ref', 'collection_exercise_sid', 'period_id', 'ref_p_start_date', 'exp', 'iat']

    decrypted_token = decrypt(token=encrypted_token,
                              key_store=current_app.eq['key_store'],
                              key_purpose=KEY_PURPOSE_AUTHENTICATION,
                              leeway=current_app.config['EQ_JWT_LEEWAY_IN_SECONDS'])

    for claim in mandatory_claims:
        if claim not in decrypted_token or not decrypted_token[claim]:
            raise InvalidTokenException('Missing mandatory values in claims - {}'.format(claim))

    logger.debug('token decrypted')
    return decrypted_token
