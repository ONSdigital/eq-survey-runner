#!/usr/bin/env python

import logging
import os
import sys

from structlog import configure
from structlog.dev import ConsoleRenderer
from structlog.processors import JSONRenderer, format_exc_info
from structlog.processors import TimeStamper
from structlog.stdlib import LoggerFactory, add_log_level
from structlog.threadlocal import wrap_dict

EQ_WERKZEUG_LOG_LEVEL = os.getenv('EQ_WERKZEUG_LOG_LEVEL', 'INFO')
EQ_DEVELOPER_LOGGING = os.getenv('EQ_DEVELOPER_LOGGING', 'False').upper() == 'TRUE'


def configure_logging():
    log_level = logging.INFO
    if os.getenv('FLASK_ENV') == 'development':
        log_level = logging.DEBUG

    info_handler = logging.StreamHandler(sys.stdout)
    info_handler.setLevel(log_level)
    info_handler.addFilter(lambda record: record.levelno <= logging.WARNING)

    error_handler = logging.StreamHandler(sys.stderr)
    error_handler.setLevel(logging.ERROR)

    logging.basicConfig(
        level=log_level, format='%(message)s', handlers=[error_handler, info_handler]
    )

    # Set werkzeug logging level
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(level=logging.getLevelName(EQ_WERKZEUG_LOG_LEVEL))

    def parse_exception(_, __, event_dict):
        if EQ_DEVELOPER_LOGGING:
            return event_dict
        exception = event_dict.get('exception')
        if exception:
            event_dict['exception'] = exception.replace('\"', "'").split('\n')
        return event_dict

    # setup file logging
    renderer_processor = ConsoleRenderer() if EQ_DEVELOPER_LOGGING else JSONRenderer()
    processors = [
        add_log_level,
        TimeStamper(key='created', fmt='iso'),
        add_service,
        format_exc_info,
        parse_exception,
        renderer_processor,
    ]

    configure(
        context_class=wrap_dict(dict),
        logger_factory=LoggerFactory(),
        processors=processors,
        cache_logger_on_first_use=True,
    )


def add_service(logger, method_name, event_dict):  # pylint: disable=unused-argument
    """
    Add the service name to the event dict.
    """
    event_dict['service'] = 'eq-survey-runner'
    return event_dict


# Initialise logging before the rest of the application
configure_logging()
from app.setup import create_app  # pylint: disable=wrong-import-position # NOQA

application = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    application.run(port=port, threaded=True)
