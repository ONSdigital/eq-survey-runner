from flask import render_template, request, redirect, json
from .. import main_blueprint
from app.main import errors
from app.authentication.jwt_decoder import Decoder
from app.authentication.invalid_token_exception import InvalidTokenException
from app.authentication.no_token_exception import NoTokenException
from app.submitter.submitter import Submitter
from app import settings
import logging
import os

EQ_URL_QUERY_STRING_JWT_FIELD_NAME = 'token'

if (settings.EQ_RRM_PUBLIC_KEY is None or settings.EQ_SR_PRIVATE_KEY is None):
    raise OSError('KEYMAT not configured correctly.')
else:
    decoder = Decoder(settings.EQ_RRM_PUBLIC_KEY, settings.EQ_SR_PRIVATE_KEY, "digitaleq")


@main_blueprint.before_request
def jwt_before_request():
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


@main_blueprint.route('/', methods=['GET'])
def root():
    return render_template('index.html')


@main_blueprint.route('/mci/', methods=['GET'])
def mci_survey():
    with main_blueprint.open_resource('data.json') as f:
        data = json.load(f)
    return render_template('mci.html', data=data)


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


@main_blueprint.route('/pattern-library/')
def index():
    return redirect("/pattern-library/styleguide/typography", code=301)


@main_blueprint.route('/pattern-library/<section>/<pattern>', methods=['GET', 'POST'])
def patterns(section='styleguide', pattern='index'):
    trimmed = {}

    def trim(str):
        trimmed_str = str.split('-', 1)[-1:][0]
        trimmed[trimmed_str] = str
        return trimmed_str

    def untrim(str):
        return trimmed[str]

    def make_section(sectionDir, dir, dirName):
        section = {
          'sections': [],
          'title': dirName
        }
        for root, dirs, files in os.walk(sectionDir):
            for file in files:
                if file.endswith('.html'):
                    # The following line causes problems with flake8, so we use `# NOQA` to ignore it
                    with open(os.path.join(root, file), 'r') as f:           # NOQA
                        title = trim(file.replace('.html', ''))
                        url = '/pattern-library/' + dirName + "/" + trim(file.replace('.html', ''))
                        section['sections'].append({
                            'url': url,
                            'title': title.replace('-', ' '),
                            'current': True if (url == pattern) else False
                        })
        return section

    with main_blueprint.open_resource('patterns.json') as f:
        data = json.load(f)

    sections = {}
    pattern_title = pattern.split('-', 1)[-1:][0]

    for root, dirs, files in os.walk('app/templates/pattern_lib/'):
        for dir in dirs:
            dirName = trim(dir)
            sections[dirName] = make_section(os.path.join(root, dir), dir, dirName)

    pattern_include = 'pattern_lib/' + untrim(section) + '/' + untrim(pattern) + '.html'
    return render_template('pattern_lib/index.html', sections=sections, pattern_include=pattern_include, title=pattern_title, data=data)
