from flask import render_template, request, json
from .. import main_blueprint
from app.main import errors
from app.authentication.jwt_decoder import Decoder
from app.authentication.invalid_token_exception import InvalidTokenException
from app.authentication.no_token_exception import NoTokenException
from app.authentication.session_management import session_manager
from app.submitter.submitter import Submitter
from app import settings

import logging


EQ_URL_QUERY_STRING_JWT_FIELD_NAME = 'token'


if settings.EQ_RRM_PUBLIC_KEY is None or settings.EQ_SR_PRIVATE_KEY is None:
    raise OSError('KEYMAT not configured correctly.')
else:
    decoder = Decoder(settings.EQ_RRM_PUBLIC_KEY, settings.EQ_SR_PRIVATE_KEY, "digitaleq")



@main_blueprint.before_request
def check_session():
    logging.debug("Checking for session")
    try:
        if request.args.get(EQ_URL_QUERY_STRING_JWT_FIELD_NAME):
            logging.debug("Authentication token", request.args.get(EQ_URL_QUERY_STRING_JWT_FIELD_NAME))
            token = jwt_login()
            logging.debug("Token authenticated - linking to session")
            session_manager.add_token(token)
        elif not session_manager.has_token():
            logging.warning("Session does not have an authenticated token - rejecting request")
            raise NoTokenException("Missing JWT")
    except NoTokenException as e:
        return errors.unauthorized(e)
    except InvalidTokenException as e:
        return errors.forbidden(e)


def jwt_login():
    if settings.EQ_PRODUCTION:
        logging.info("Production mode")
        return jwt_decrypt()
    else:
        logging.warning("Developer mode")
        return developer_mode()


def developer_mode():
    token = request.args.get(EQ_URL_QUERY_STRING_JWT_FIELD_NAME)
    if token:
        if token.count(".") == 4:
            logging.debug("Decrypting JWT token " + token)
            return jwt_decrypt()
        else:
            tokens = token.split(".")
            if len(tokens) == 3 and tokens[2]:
                logging.debug("Decoding signed JWT token " + token)
                return jwt_decode_signed()
            else:
                logging.debug("Decoding JWT token " + token)
                return jwt_decode()


def jwt_decrypt():
    encrypted_token = request.args.get(EQ_URL_QUERY_STRING_JWT_FIELD_NAME)
    token = decoder.decrypt_jwt_token(encrypted_token)
    send_to_mq(token)
    return token


def jwt_decode_signed():
    signed_token = request.args.get(EQ_URL_QUERY_STRING_JWT_FIELD_NAME)
    token = decoder.decode_signed_jwt_token(signed_token)
    send_to_mq(token)
    return token


def jwt_decode():
    unsigned_token = request.args.get(EQ_URL_QUERY_STRING_JWT_FIELD_NAME)
    token = decoder.decode_jwt_token(unsigned_token)
    send_to_mq(token)
    return token


@main_blueprint.route('/', methods=['GET'])
def root():
    return render_template('index.html')


@main_blueprint.route('/questionnaire/mci/', methods=['GET'])
def mci_survey():
    with main_blueprint.open_resource('../data/mci.json') as f:
        data = json.load(f)
    return render_template('questionnaire.html', questionnaire=data)


@main_blueprint.route('/cover-page', methods=['GET'])
def cover_page():
    return render_template('cover-page.html')


@main_blueprint.route('/jwt', methods=['GET'])
def jwt():
    return jwt_decode()


@main_blueprint.route('/jwt_signed', methods=['GET'])
def jwt_signed():
    return jwt_decode_signed()


@main_blueprint.route('/jwt_encrypted', methods=['GET'])
def jwt_encrypted_key_exchange():
    return jwt_decrypt()


def send_to_mq(token):
    submitter = Submitter()
    submitter.send(token)
