from app.authentication.jwt_decoder import Decoder
from app.authentication.session_management import session_manager
from app.authentication.no_token_exception import NoTokenException
from app.authentication.invalid_token_exception import InvalidTokenException
from app.authentication.user import User
import logging

EQ_URL_QUERY_STRING_JWT_FIELD_NAME = 'token'

logger = logging.getLogger(__name__)


class Authenticator(object):

    def check_session(self):
        """
        Checks for the present of the JWT in the users sessions
        :return: A user object if a JWT token is available in the session
        """
        logger.debug("Checking for session")
        if session_manager.has_token():
            logger.debug("Session token exists")
            return User(session_manager.get_token())
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

        # once we've decrypted the token correct
        # check we have the required user data
        self._check_user_data(token)

        # store the token in the session
        session_manager.add_token(token)
        return token

    def _jwt_decrypt(self, request):
        encrypted_token = request.args.get(EQ_URL_QUERY_STRING_JWT_FIELD_NAME)
        decoder = Decoder()
        token = decoder.decrypt_jwt_token(encrypted_token)
        return token

    def _check_user_data(self, token):
        user = User(token)
        valid, reason = user.is_valid()
        if not valid:
            raise InvalidTokenException("Missing value {}".format(reason))
