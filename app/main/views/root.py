from flask import render_template, request, redirect, json, Response
from .. import main
from app.main import errors
from app.authentication.jwt_decoder import Decoder
from app.authentication.invalid_token_exception import InvalidTokenException
from app.authentication.no_token_exception import NoTokenException
from app.submitter.submitter import Submitter
from app import settings
import logging
import os

EQ_URL_QUERY_STRING_JWT_FIELD_NAME = 'token'

if settings.EQ_PRODUCTION.upper() != 'FALSE':
    if (settings.EQ_RRM_PUBLIC_KEY is None or settings.EQ_SR_PRIVATE_KEY is None):
        raise OSError('KEYMAT not configured correctly.')
    else:
        decoder = Decoder(settings.EQ_RRM_PUBLIC_KEY, settings.EQ_SR_PRIVATE_KEY, "digitaleq")


@main.before_request
def jwt():
    if settings.EQ_PRODUCTION.upper() != 'FALSE':
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
    try:
        encrypted_token = request.args.get(EQ_URL_QUERY_STRING_JWT_FIELD_NAME)
        token = decoder.decrypt_jwt_token(encrypted_token)
        send_to_mq(token)
        return render_template('index.html', token_id=encrypted_token, token=token)
    except NoTokenException as e:
        return errors.unauthorized(e)
    except InvalidTokenException as e:
        return errors.forbidden(e)


def jwt_decode_signed():
    try:
        signed_token = request.args.get(EQ_URL_QUERY_STRING_JWT_FIELD_NAME)
        token = decoder.decode_signed_jwt_token(signed_token)
        send_to_mq(token)
        return render_template('index.html', token_id=signed_token, token=token)
    except NoTokenException as e:
        return errors.unauthorized(e)
    except InvalidTokenException as e:
        return errors.forbidden(e)


def jwt_decode():
    try:
        unsigned_token = request.args.get(EQ_URL_QUERY_STRING_JWT_FIELD_NAME)
        token = decoder.decode_jwt_token(unsigned_token)
        send_to_mq(token)
        return render_template('index.html', token_id=unsigned_token, token=token)
    except NoTokenException as e:
        return errors.unauthorized(e)
    except InvalidTokenException as e:
        return errors.forbidden(e)


@main.route('/', methods=['GET'])
def root():
    return render_template('index.html')


@main.route('/mci/', methods=['GET'])
def mci_survey():
    return render_template('mci.html')


@main.route('/jwt', methods=['GET'])
def jwt():
    return jwt_decode()


@main.route('/jwt_signed', methods=['GET'])
def jwt_signed():
    return jwt_decode_signed()


@main.route('/jwt_encrypted', methods=['GET'])
def jwt_encrypted_key_exchange():
    return jwt_decrypt()


def send_to_mq(token):
    submitter = Submitter()
    submitter.send(token)


@main.route('/patterns/')
def index():
    return redirect("/patterns/1-typography", code=301)


@main.route('/patterns/<pattern>/', methods=['GET', 'POST'])
def patterns(pattern='index'):
    sections = []
    pattern_title = pattern.split("-", 1)[-1:][0]
    for root, dirs, files in os.walk('app/templates/patterns/components'):
        for file in files:
            if file.endswith('.html'):
                with open(os.path.join(root, file), 'r') as f:
                    title = file.replace('.html', '').split("-", 1)[-1:][0]
                    url = file.replace('.html', '')
                    sections.append({
                        'url': url,
                        'title': title.replace('-', ' '),
                        'current': True if (url == pattern) else False
                    })
    return render_template('patterns/index.html', sections=sections, pattern_include='patterns/components/' + pattern + '.html', title=pattern_title)


@main.route('/validate/', methods=['GET', 'POST'])
def validate():
    data = {'msg': 'Wrong!'}
    status = 404
    if request.form['q'] == 'hello':
        data = {'msg': 'Correct!'}
        status = 200
    js = json.dumps(data)
    return Response(js, status=status, mimetype='application/json')
