#!/usr/bin/env python

import logging
import os
from logging.handlers import RotatingFileHandler

import watchtower
from flask_script import Manager
from flask_script import Server
from structlog import configure
from structlog.dev import ConsoleRenderer
from structlog.processors import JSONRenderer, format_exc_info
from structlog.processors import TimeStamper
from structlog.stdlib import LoggerFactory, add_log_level
from structlog.threadlocal import wrap_dict

EQ_SR_LOG_GROUP = os.getenv('EQ_SR_LOG_GROUP', os.getenv('USER', 'UNKNOWN') + '-local')
EQ_LOG_LEVEL = os.getenv('EQ_LOG_LEVEL', 'INFO')
EQ_CLOUDWATCH_LOGGING = os.getenv("EQ_CLOUDWATCH_LOGGING", 'True').upper() == 'TRUE'
EQ_WERKZEUG_LOG_LEVEL = os.getenv('EQ_WERKZEUG_LOG_LEVEL', 'INFO')
EQ_DEVELOPER_LOGGING = os.getenv('EQ_DEVELOPER_LOGGING', 'False').upper() == 'TRUE'


def _setup_cloud_watch_logging():

    # filter out botocore messages, we don't wish to log these
    class NoBotocoreFilter(logging.Filter):

        def filter(self, record):
            return not record.name.startswith('botocore')

    cloud_watch_handler = watchtower.CloudWatchLogHandler(log_group=EQ_SR_LOG_GROUP)
    cloud_watch_handler.addFilter(NoBotocoreFilter())
    logging.getLogger().addHandler(cloud_watch_handler)
    # we DO NOT WANT the root logger logging to cloudwatch as thsi causes
    # weird recursion errors
    logging.getLogger().addHandler(cloud_watch_handler)  # root logger
    logging.getLogger(__name__).addHandler(cloud_watch_handler)  # module logger
    logging.getLogger('werkzeug').addHandler(
        cloud_watch_handler)  # werkzeug framework logger


def configure_logging():
    # set up some sane logging, as opposed to what flask does by default
    log_format = "%(message)s"
    levels = {
        'CRITICAL': logging.CRITICAL,
        'ERROR': logging.ERROR,
        'WARNING': logging.WARNING,
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG,
    }
    handler = logging.StreamHandler()
    logging.basicConfig(level=levels[EQ_LOG_LEVEL], format=log_format, handlers=[handler])

    # turn boto logging to critical as it logs far too much and it's only used
    # for cloudwatch logging
    logging.getLogger("botocore").setLevel(logging.ERROR)
    if EQ_CLOUDWATCH_LOGGING:
        _setup_cloud_watch_logging()

    # Set werkzeug logging level
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(level=levels[EQ_WERKZEUG_LOG_LEVEL])

    # setup file logging
    rotating_log_file = RotatingFileHandler(filename="eq.log", maxBytes=1048576, backupCount=10)
    logging.getLogger().addHandler(rotating_log_file)
    renderer_processor = ConsoleRenderer() if EQ_DEVELOPER_LOGGING else JSONRenderer()
    processors = [add_log_level, TimeStamper(key='created', fmt='iso'), add_service, format_exc_info, renderer_processor]
    configure(context_class=wrap_dict(dict), logger_factory=LoggerFactory(), processors=processors, cache_logger_on_first_use=True)


def add_service(logger, method_name, event_dict):  # pylint: disable=unused-argument
    """
    Add the service name to the event dict.
    """
    event_dict['service'] = 'eq-survey-runner'
    return event_dict

# Initialise logging before the rest of the application
configure_logging()
from app import create_app  # NOQA
application = create_app()

manager = Manager(application)
port = int(os.environ.get('PORT', 5000))
manager.add_command("runserver", Server(host='0.0.0.0', port=port))


if __name__ == '__main__':
    manager.run()
