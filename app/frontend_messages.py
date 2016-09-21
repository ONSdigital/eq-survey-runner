from flask.ext.babel import gettext as _


MESSAGES = {
            'multiple-surveys': {
                'TITLE': _("Information"),
                'MSG': _("Unfortunately you can only complete one survey at a time."),
                'INSTRUCTIONS': _("Close this window to continue with your current survey."),
                },
            }


def get_message(message):
    if message in MESSAGES:
        return MESSAGES['multiple-surveys']

