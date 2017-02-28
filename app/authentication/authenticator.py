from flask import session
from flask_login import LoginManager
from structlog import get_logger

from app.authentication.invalid_token_exception import InvalidTokenException
from app.authentication.jwt_decoder import JWTDecryptor
from app.authentication.no_token_exception import NoTokenException
from app.authentication.session_storage import session_storage
from app.authentication.user import User
from app.authentication.user_id_generator import UserIDGenerator
from app.globals import get_questionnaire_store
from app.parser.metadata_parser import is_valid_metadata, parse_metadata

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
    user_id = session_storage.get_user_id()
    if user_id:
        user = User(user_id, session_storage.get_user_ik())
        questionnaire_store = get_questionnaire_store(user.user_id, user.user_ik)
        metadata = questionnaire_store.metadata
        logger.bind(tx_id=metadata["tx_id"])
        logger.debug("session token exists")

        return user
    else:
        logger.info("session does not have an authenticated token")
        return None


def jwt_login(request):
    """
    Login using a JWT token, this must be an encrypted JWT.
    :param request: The flask request
    """
    # clear the session entry in the database
    session_storage.clear()
    # also clear the secure cookie data
    session.clear()

    encrypted_token = request.args.get('token')

    if encrypted_token is None:
        raise NoTokenException("Please provide a token")

    decrypted_token = jwt_decrypt(encrypted_token)

    # once we've decrypted the token correct
    # check we have the required user data
    _check_user_data(decrypted_token)

    # get the hashed user id for eq
    user_id = UserIDGenerator.generate_id(decrypted_token)
    user_ik = UserIDGenerator.generate_ik(decrypted_token)

    # store the user id in the session
    session_storage.store_user_id(user_id)
    # store the user ik in the cookie
    session_storage.store_user_ik(user_ik)

    # store the meta data
    metadata = parse_metadata(decrypted_token)
    logger.bind(tx_id=metadata["tx_id"])

    questionnaire_store = get_questionnaire_store(user_id, user_ik)
    questionnaire_store.metadata = metadata
    questionnaire_store.add_or_update()
    logger.info("user authenticated")


def jwt_decrypt(encrypted_token):
    decoder = JWTDecryptor()
    decrypted_token = decoder.decrypt_jwt_token(encrypted_token)
    return decrypted_token


def _check_user_data(token):
    valid, field = is_valid_metadata(token)
    if not valid:
        raise InvalidTokenException("Missing value {}".format(field))
