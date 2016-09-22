import logging

from flask.ext.babel import gettext as _

logger = logging.getLogger(__name__)

MESSAGES = {
            'multiple-surveys': {
                'TITLE': _("Information"),
                'MSG': _("Unfortunately you can only complete one survey at a time."),
                'INSTRUCTIONS': _("Close this window to continue with your current survey."),
                },
            }


def get_messages(system_message):
    if system_message in MESSAGES:
        return MESSAGES['multiple-surveys']
    logger.debug("Message not found %s", system_message)
    return None
