#!/usr/bin/env python

import os
from app import create_app
from flask.ext.script import Manager, Server

import watchtower
import logging
import app.settings as settings


application = create_app(
    os.getenv('EQ_ENVIRONMENT') or 'development'
)
application.debug = True

manager = Manager(application)
port = int(os.environ.get('PORT', 5000))
manager.add_command("runserver", Server(host='0.0.0.0', port=port))

FORMAT = "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"
levels = {
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG
}
logging.basicConfig(level=levels[settings.EQ_LOG_LEVEL], format=FORMAT)

if settings.EQ_PRODUCTION:
    log_group = settings.EQ_SR_LOG_GROUP
    cloud_watch_handler = watchtower.CloudWatchLogHandler(log_group=log_group)
    application.logger.addHandler(cloud_watch_handler)
    logging.getLogger().addHandler(cloud_watch_handler)
    logging.getLogger(__name__).addHandler(cloud_watch_handler)
    logging.getLogger('werkzeug').addHandler(cloud_watch_handler)
else:
    console_handler = logging.StreamHandler()
    application.logger.addHandler(console_handler)
    logging.getLogger().addHandler(console_handler)
    logging.getLogger(__name__).addHandler(console_handler)
    logging.getLogger('werkzeug').addHandler(console_handler)

if __name__ == '__main__':
    manager.run()
