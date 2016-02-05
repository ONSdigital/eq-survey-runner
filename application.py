#!/usr/bin/env python

import os
from app import create_app
from app import settings

from flask.ext.script import Manager, Server

if not settings.EQ_PRODUCTION:
    with open(os.getcwd() + '/jwt-test-keys/rrm-public.pem', "rb") as public_key_file:
        settings.EQ_RRM_PUBLIC_KEY = public_key_file.read()
    with open(os.getcwd() + '/jwt-test-keys/sr-private.pem', "rb") as private_key_file:
        settings.EQ_SR_PRIVATE_KEY = private_key_file.read()

application = create_app(
    os.getenv('SR_ENVIRONMENT') or 'development'
)
application.debug = True
manager = Manager(application)
port = int(os.environ.get('PORT', 5000))
manager.add_command("runserver", Server(host='0.0.0.0', port=port))

if __name__ == '__main__':
    manager.run()
