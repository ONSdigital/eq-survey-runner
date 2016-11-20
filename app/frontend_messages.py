import logging

from flask.ext.babel import gettext as _

logger = logging.getLogger(__name__)

MESSAGES = {
    'multiple-surveys': {
        'title': _("Information"),
        'message': _("Unfortunately you can only complete one survey at a time."),
        'instructions': _("Close this window to continue with your current survey."),
    },
}


def get_messages(message_identifier):
    if message_identifier in MESSAGES:
        return MESSAGES[message_identifier]
    logger.debug("Message not found %s", message_identifier)
    return None
