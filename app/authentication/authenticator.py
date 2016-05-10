import logging

from app.authentication.invalid_token_exception import InvalidTokenException
from app.authentication.jwt_decoder import JWTDecryptor
from app.authentication.no_token_exception import NoTokenException
from app.authentication.session_management import session_manager
from app.authentication.user import User
from app.metadata.metadata_store import MetaDataStore
from app.utilities.factory import factory


EQ_URL_QUERY_STRING_JWT_FIELD_NAME = 'token'

logger = logging.getLogger(__name__)


class Authenticator(object):

    def check_session(self):
        """
        Checks for the present of the JWT in the users sessions
        :return: A user object if a JWT token is available in the session
        """
        logger.debug("Checking for session")
        if session_manager.has_user_id():
            logger.debug("Session token exists")
            return User(session_manager.get_user_id())
        else:
            logging.debug("Session does not have an authenticated token")
            return None

    def jwt_login(self, request):
        """
        Login using a JWT token, this must be an encrypted JWT.
        :param request: The flask request
        :return: the decrypted and unencoded token
        """
        if request.args.get(EQ_URL_QUERY_STRING_JWT_FIELD_NAME) is None:
            raise NoTokenException("Please provide a token")
        token = self._jwt_decrypt(request)

        # <kludge>
        # TODO: Remove this once RM is correctly sending dates
        from app.metadata.metadata_store import MetaDataConstants
        token[MetaDataConstants.REF_P_START_DATE] = '2016-04-03'
        token[MetaDataConstants.REF_P_END_DATE] = '2016-04-30'
        # </kludge>

        # once we've decrypted the token correct
        # check we have the required user data
        self._check_user_data(token)

        user_id = token.get(MetaDataConstants.USER_ID)

        # store the user id in the session
        session_manager.store_user_id(user_id)

        # store the meta data
        metadata_store = factory.create("metadata-store")

        metadata_store.store_all(token)

        return User(user_id)

    def _jwt_decrypt(self, request):
        encrypted_token = request.args.get(EQ_URL_QUERY_STRING_JWT_FIELD_NAME)
        decoder = JWTDecryptor()
        token = decoder.decrypt_jwt_token(encrypted_token)
        return token

    def _check_user_data(self, token):
        valid, reason = MetaDataStore.is_valid(token)
        if not valid:
            raise InvalidTokenException("Missing value {}".format(reason))
