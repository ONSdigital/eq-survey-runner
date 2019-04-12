from datetime import datetime, timedelta
from uuid import uuid4

from blinker import ANY
from dateutil.tz import tzutc
from flask import session as cookie_session, current_app
from flask_login import LoginManager, user_logged_out
from sdc.crypto.decrypter import decrypt
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


def _extend_session_expiry(session_store):
    """
    Extends the expiration time of the session
    :param session_store:
    """
    session_timeout = cookie_session.get('expires_in')
    if session_timeout:
        new_expiration_time = datetime.now(tz=tzutc()) + timedelta(seconds=session_timeout)

        # Only update expiry time if its greater than 60s different to what is currently set
        if not session_store.expiration_time or (new_expiration_time - session_store.expiration_time).total_seconds() > 60:
            session_store.expiration_time = new_expiration_time
            session_store.save()
            logger.debug('session expiry extended')


def _is_session_valid(session_store):
    """
    Checks that the user's session has not expired
    :param session_store:
    :return: True if the session is valid else False
    """

    if session_store.expiration_time and \
            session_store.expiration_time < datetime.now(tz=tzutc()):
        return False

    return True


def load_user():
    """
    Checks for the present of the JWT in the users sessions
    :return: A user object if a JWT token is available in the session
    """
    session_store = get_session_store()

    if session_store and session_store.user_id and _is_session_valid(session_store):
        logger.debug('session exists')

        user_id = session_store.user_id
        user_ik = cookie_session.get(USER_IK)
        user = User(user_id, user_ik)

        if session_store.session_data.tx_id:
            logger.bind(tx_id=session_store.session_data.tx_id)

        _extend_session_expiry(session_store)

        return user

    logger.info('session does not exist')

    cookie_session.pop(USER_IK, None)
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
        trad_as=metadata.get('trad_as'),
        account_service_url=metadata.get('account_service_url'),
        account_service_log_out_url=metadata.get('account_service_log_out_url'),
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
    questionnaire_store.set_metadata(metadata)
    questionnaire_store.add_or_update()

    logger.info('user authenticated')


def decrypt_token(encrypted_token):
    if not encrypted_token:
        raise NoTokenException('Please provide a token')

    logger.debug('decrypting token')
    decrypted_token = decrypt(token=encrypted_token,
                              key_store=current_app.eq['key_store'],
                              key_purpose=KEY_PURPOSE_AUTHENTICATION,
                              leeway=current_app.config['EQ_JWT_LEEWAY_IN_SECONDS'])

    logger.debug('token decrypted')
    return decrypted_token
