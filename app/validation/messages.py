from flask.ext.babel import gettext as _

# Set up default error and warning messages
messages = {
    'NOT_INTEGER': _("Please only enter whole numbers into the field."),
    'NOT_STRING': _("This is not a string."),
    'MANDATORY': _("This field is mandatory."),
    'INVALID_DATE': _("This is not a valid date."),
    'NEGATIVE_INTEGER': _("Negative values are not allowed."),
    'INTEGER_TOO_LARGE': _('This number is too big.'),
    'INVALID_DATE_RANGE_TO_BEFORE_FROM': _("The 'to' date cannot be before the 'from' date."),
    'INVALID_DATE_RANGE_TO_FROM_SAME': _("The 'to' date must be different to the 'from' date.")
}
