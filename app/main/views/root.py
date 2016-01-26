import os
import markdown
import yaml
from flask import render_template, render_template_string, session, request
from .. import main
from application import application
from app.main import errors
from app.authentication.jwt_decoder import Decoder, NoTokenException, InvalidTokenException


# TODO Put this back in
# @main.before_request
def authenticate():
    try:
        encrypted_token = request.args.get('token')
        print('Encrypted token ' + encrypted_token)
        token = Decoder().decrypt_token(encrypted_token)
        return token
    except NoTokenException as e:
        return errors.unauthorized(e)
    except InvalidTokenException as e:
        return errors.forbidden(e)


def jwt_decode():
    try:
        signed_token = request.args.get('token')
        token = Decoder().decode_jwt_token(signed_token)
        return token
    except NoTokenException as e:
        return errors.unauthorized(e)
    except InvalidTokenException as e:
        return errors.forbidden(e)


@main.route('/', methods=['GET'])
def root():
    return render_template('index.html')


@main.route('/jwt', methods=['GET'])
def jwt():
    # TODO not signed jwt
    return render_template('index.html')


@main.route('/signed', methods=['GET'])
def jwt_signed():
    jwt_decode()
    return render_template('index.html')


@main.route('/encrypted-key-exchange', methods=['GET'])
def jwt_encrypted_key_exchange():
    # TODO implement Key exchange
    authenticate()
    return render_template('index.html')


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
