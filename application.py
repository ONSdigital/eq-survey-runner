#!/usr/bin/env python

import os
from app import create_app
from flask.ext.script import Manager, Server
import watchtower
import logging


application = create_app(
    os.getenv('EQ_ENVIRONMENT') or 'development'
)
application.debug = True
manager = Manager(application)
port = int(os.environ.get('PORT', 5000))
manager.add_command("runserver", Server(host='0.0.0.0', port=port))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(watchtower.CloudWatchLogHandler())


if __name__ == '__main__':
    manager.run()
