import os
import markdown
import yaml
from flask import render_template, render_template_string, session, request
from .. import main
from application import application
from app.main import errors
from app.authentication.jwt_decoder import Decoder, NoTokenException, InvalidTokenException


with open("rrm-public.pem", "rb") as public_key_file:
    rmm_public_key = public_key_file.read()

with open("sr-private.pem", "rb") as private_key_file:
    sr_private_key = private_key_file.read()

decoder = Decoder(rmm_public_key, sr_private_key, "digitaleq")


# TODO Put this back in
# @main.before_request
def jwt_decrypt():
    try:
        encrypted_token = request.args.get('token')
        print('Encrypted token ' + encrypted_token)
        token = decoder.decrypt_jwt_token(encrypted_token)
        print(token)
        return render_template('index.html')
    except NoTokenException as e:
        return errors.unauthorized(e)
    except InvalidTokenException as e:
        return errors.forbidden(e)


def jwt_decode_signed():
    try:
        signed_token = request.args.get('token')
        token = decoder.decode_signed_jwt_token(signed_token)
        print(token)
        return render_template('index.html')
    except NoTokenException as e:
        return errors.unauthorized(e)
    except InvalidTokenException as e:
        return errors.forbidden(e)


def jwt_decode():
    try:
        token = request.args.get('token')
        token = decoder.decode_jwt_token(token)
        print(token)
        return render_template('index.html')
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

@main.route('/patterns/')
@main.route('/patterns/<pattern>')
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
