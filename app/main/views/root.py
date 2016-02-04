from flask import render_template, request, json, Response
from .. import main
from app.main import errors
from app.authentication.jwt_decoder import Decoder
from app.authentication.invalid_token_exception import InvalidTokenException
from app.authentication.no_token_exception import NoTokenException
from app.submitter.submitter import Submitter
from app import settings
import os


with open(settings.EQ_RRM_PUBLIC_KEY, "rb") as public_key_file:
    rmm_public_key = public_key_file.read()

with open(settings.EQ_SR_PRIVATE_KEY, "rb") as private_key_file:
    sr_private_key = private_key_file.read()

decoder = Decoder(rmm_public_key, sr_private_key, "digitaleq")


# @main.before_request
def jwt_decrypt():
    try:
        encrypted_token = request.args.get('token')
        token = decoder.decrypt_jwt_token(encrypted_token)
        send_to_mq(token)
        return render_template('index.html', token_id=encrypted_token, token=token)
    except NoTokenException as e:
        return errors.unauthorized(e)
    except InvalidTokenException as e:
        return errors.forbidden(e)


def jwt_decode_signed():
    try:
        signed_token = request.args.get('token')
        token = decoder.decode_signed_jwt_token(signed_token)
        send_to_mq(token)
        return render_template('index.html', token_id=signed_token, token=token)
    except NoTokenException as e:
        return errors.unauthorized(e)
    except InvalidTokenException as e:
        return errors.forbidden(e)


def jwt_decode():
    try:
        jwt = request.args.get('token')
        token = decoder.decode_jwt_token(jwt)
        send_to_mq(token)
        return render_template('index.html', token_id=jwt, token=token)
    except NoTokenException as e:
        return errors.unauthorized(e)
    except InvalidTokenException as e:
        return errors.forbidden(e)


@main.route('/', methods=['GET'])
def root():
    return render_template('index.html')


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
@main.route('/patterns/<pattern>', methods=['GET', 'POST'])
def patterns(pattern='index'):
    sections = []
    pattern_name = 'grid-system' if (pattern == 'index') else pattern
    for root, dirs, files in os.walk('app/templates/patterns/components'):
        for file in files:
            if file.endswith('.html'):
                with open(os.path.join(root, file), 'r') as f:
                    title = file.replace('.html', '')
                    sections.append({
                        'title': title,
                        'current': True if (title == pattern) else False
                    })
    return render_template('patterns/index.html', sections=sections, pattern_include='patterns/components/' + pattern_name + '.html', title=pattern)


@main.route('/validate/', methods=['GET', 'POST'])
def validate():
    data = {'msg': 'Wrong!'}
    status = 404
    if request.form['q'] == 'hello':
        data = {'msg': 'Correct!'}
        status = 200
    js = json.dumps(data)
    return Response(js, status=status, mimetype='application/json')
