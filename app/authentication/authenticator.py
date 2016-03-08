from app.authentication.jwt_decoder import Decoder
from app.authentication.session_management import session_manager
from app.authentication.no_token_exception import NoTokenException
from app import settings
from flask.ext.login import UserMixin
import logging

EQ_URL_QUERY_STRING_JWT_FIELD_NAME = 'token'

logger = logging.getLogger(__name__)


class User(UserMixin):
    def __init__(self, id):
        self.id = id


class Authenticator(object):

    def check_session(self, request):
        logger.debug("Checking for session")
        if session_manager.has_token():
            logger.debug("Session token exists")
            return User(session_manager.get_token())
        else:
            logging.debug("Session does not have an authenticated token")
            return None

    def jwt_login(self, request):
        if settings.EQ_PRODUCTION:
            logger.info("Production mode")
            if request.args.get(EQ_URL_QUERY_STRING_JWT_FIELD_NAME) is None:
                raise NoTokenException("Please provide a token")
            return self._jwt_decrypt(request)
        else:
            logger.warning("Developer mode")
            return self._developer_mode_login(request)

    def _developer_mode_login(self, request):
        token = request.args.get(EQ_URL_QUERY_STRING_JWT_FIELD_NAME)
        if token:
            if token.count(".") == 4:
                logger.debug("Decrypting JWT token " + token)
                return self._jwt_decrypt(request)
            else:
                tokens = token.split(".")
                if len(tokens) == 3 and tokens[2]:
                    logger.debug("Decoding signed JWT token " + token)
                    return self._jwt_decode_signed(request)
                else:
                    logger.debug("Decoding JWT token " + token)
                    return self._jwt_decode(request)
        else:
            return "developer-mode"

    def _jwt_decrypt(self, request):
        encrypted_token = request.args.get(EQ_URL_QUERY_STRING_JWT_FIELD_NAME)
        decoder = Decoder()
        token = decoder.decrypt_jwt_token(encrypted_token)
        return token

    def _jwt_decode_signed(self, request):
        signed_token = request.args.get(EQ_URL_QUERY_STRING_JWT_FIELD_NAME)
        decoder = Decoder()
        token = decoder.decode_signed_jwt_token(signed_token)
        return token

    def _jwt_decode(self, request):
        unsigned_token = request.args.get(EQ_URL_QUERY_STRING_JWT_FIELD_NAME)
        decoder = Decoder()
        token = decoder.decode_jwt_token(unsigned_token)
        return token
