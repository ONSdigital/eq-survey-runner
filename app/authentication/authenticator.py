from flask import session
from flask import current_app
from flask_login import LoginManager
from structlog import get_logger

from app.authentication.invalid_token_exception import InvalidTokenException
from app.authentication.no_token_exception import NoTokenException
from app.authentication.user import User
from app.globals import get_questionnaire_store
from app.secrets import KEY_PURPOSE_AUTHENTICATION
from app.storage.metadata_parser import is_valid_metadata

from sdc.crypto.decrypter import decrypt

logger = get_logger()

login_manager = LoginManager()


@login_manager.user_loader
def user_loader(user_id):
    logger.debug("loading user", user_id=user_id)
    return load_user()


@login_manager.request_loader
def request_load_user(request):  # pylint: disable=unused-argument
    logger.debug("load user")
    return load_user()


def load_user():
    """
    Checks for the present of the JWT in the users sessions
    :return: A user object if a JWT token is available in the session
    """
    user_id = current_app.eq['session_storage'].get_user_id()
    if user_id:
        user = User(user_id, current_app.eq['session_storage'].get_user_ik())
        questionnaire_store = get_questionnaire_store(user.user_id, user.user_ik)
        metadata = questionnaire_store.metadata
        if metadata:
            logger.bind(tx_id=metadata["tx_id"])
        logger.debug("session token exists")

        return user
    else:
        logger.info("session does not have an authenticated token")
        return None


def store_session(metadata):
    """
    Store new session and metadata
    :param metadata: metadata parsed from jwt token
    """
    # clear the session entry in the database
    current_app.eq['session_storage'].delete_session_from_db()

    # also clear the secure cookie data
    session.clear()

    # get the hashed user id for eq
    id_generator = current_app.eq['id_generator']
    user_id = id_generator.generate_id(metadata)
    user_ik = id_generator.generate_ik(metadata)

    # store the user id in the session

    current_app.eq['session_storage'].store_user_id(user_id)
    # store the user ik in the cookie
    current_app.eq['session_storage'].store_user_ik(user_ik)

    questionnaire_store = get_questionnaire_store(user_id, user_ik)
    questionnaire_store.metadata = metadata
    questionnaire_store.add_or_update()
    logger.info("user authenticated")


def decrypt_token(encrypted_token):
    logger.debug("decrypting token")
    if not encrypted_token or encrypted_token is None:
        raise NoTokenException("Please provide a token")

    decrypted_token = decrypt(token=encrypted_token,
                              key_store=current_app.eq['secret_store'],
                              key_purpose=KEY_PURPOSE_AUTHENTICATION,
                              leeway=current_app.config['EQ_JWT_LEEWAY_IN_SECONDS'])

    valid, field = is_valid_metadata(decrypted_token)
    if not valid:
        raise InvalidTokenException("Missing value {}".format(field))

    logger.debug("token decrypted")
    return decrypted_token
