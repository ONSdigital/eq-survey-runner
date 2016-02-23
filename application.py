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

cloud_watch_handler = watchtower.CloudWatchLogHandler()

logging.basicConfig(level=logging.INFO)
application.logger.addHandler(cloud_watch_handler)
logging.getLogger().addHandler(cloud_watch_handler)
logging.getLogger(__name__).addHandler(cloud_watch_handler)
logging.getLogger('werkzeug').addHandler(cloud_watch_handler)


if __name__ == '__main__':
    manager.run()
