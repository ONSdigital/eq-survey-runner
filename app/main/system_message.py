import logging

from flask.ext.themes2 import render_theme_template

logger = logging.getLogger(__name__)


def system_message(messages):
    logger.debug(messages)
    return render_theme_template('default', 'system_message.html',
                                 messages=messages)
