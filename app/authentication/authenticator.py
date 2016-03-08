from app.authentication.jwt_decoder import Decoder
from app.authentication.session_management import session_manager
from app.authentication.no_token_exception import NoTokenException
from app.authentication.invalid_token_exception import InvalidTokenException
from app import settings
from flask import current_app
from flask.ext.login import UserMixin
import logging

EQ_URL_QUERY_STRING_JWT_FIELD_NAME = 'token'


class User(UserMixin):
    def __init__(self, id):
        self.id = id


def check_session(request):
    current_app.logger.debug("Checking for session")
    if request.args.get(EQ_URL_QUERY_STRING_JWT_FIELD_NAME):
        current_app.logger.debug("Authentication token", request.args.get(EQ_URL_QUERY_STRING_JWT_FIELD_NAME))
        try:
            token = jwt_login(request)
            current_app.logger.debug("Token authenticated - linking to session")
            session_manager.add_token(token)
            return User(token)
        except NoTokenException as e:
            current_app.logger.warning("Unable to authenticate user", e)
            return None
        except InvalidTokenException as e:
            current_app.logger.warning("Invalid Token provided", e)
            return None
    elif session_manager.has_token():
        return User(session_manager.get_token())
    else:
        logging.debug("Session does not have an authenticated token")
        return None


def jwt_login(request):
    if settings.EQ_PRODUCTION:
        current_app.logger.info("Production mode")
        return jwt_decrypt(request)
    else:
        current_app.logger.warning("Developer mode")
        return developer_mode_login(request)


def developer_mode_login(request):
    token = request.args.get(EQ_URL_QUERY_STRING_JWT_FIELD_NAME)
    if token:
        if token.count(".") == 4:
            current_app.logger.debug("Decrypting JWT token " + token)
            return jwt_decrypt(request)
        else:
            tokens = token.split(".")
            if len(tokens) == 3 and tokens[2]:
                current_app.logger.debug("Decoding signed JWT token " + token)
                return jwt_decode_signed(request)
            else:
                current_app.logger.debug("Decoding JWT token " + token)
                return jwt_decode(request)


def jwt_decrypt(request):
    encrypted_token = request.args.get(EQ_URL_QUERY_STRING_JWT_FIELD_NAME)
    decoder = Decoder()
    token = decoder.decrypt_jwt_token(encrypted_token)
    return token


def jwt_decode_signed(request):
    signed_token = request.args.get(EQ_URL_QUERY_STRING_JWT_FIELD_NAME)
    decoder = Decoder()
    token = decoder.decode_signed_jwt_token(signed_token)
    return token


def jwt_decode(request):
    unsigned_token = request.args.get(EQ_URL_QUERY_STRING_JWT_FIELD_NAME)
    decoder = Decoder()
    token = decoder.decode_jwt_token(unsigned_token)
    return token
