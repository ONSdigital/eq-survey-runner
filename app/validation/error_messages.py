from flask_babel import lazy_gettext

# Set up default error and warning messages
# lazy_gettext is used as the string needs to be resolved at runtime
# for translations to work.
error_messages = {
    'MANDATORY_QUESTION': lazy_gettext('Enter an answer to continue.'),
    'MANDATORY_TEXTFIELD': lazy_gettext('Enter an answer to continue.'),
    'MANDATORY_NUMBER': lazy_gettext('Enter an answer to continue.'),
    'MANDATORY_TEXTAREA': lazy_gettext('Enter an answer to continue.'),
    'MANDATORY_RADIO': lazy_gettext('Select an answer to continue.'),
    'MANDATORY_DROPDOWN': lazy_gettext('Select an answer to continue.'),
    'MANDATORY_CHECKBOX': lazy_gettext('Select all that apply to continue.'),
    'MANDATORY_DATE': lazy_gettext('Enter a date to continue.'),
    'MANDATORY_DURATION': lazy_gettext('Enter a duration to continue.'),
    'NUMBER_TOO_SMALL': lazy_gettext('Enter an answer more than or equal to %(min)s.'),
    'NUMBER_TOO_LARGE': lazy_gettext('Enter an answer less than or equal to %(max)s.'),
    'NUMBER_TOO_SMALL_EXCLUSIVE': lazy_gettext('Enter an answer more than %(min)s.'),
    'NUMBER_TOO_LARGE_EXCLUSIVE': lazy_gettext('Enter an answer less than %(max)s.'),
    'TOTAL_SUM_NOT_EQUALS': lazy_gettext('Enter answers that add up to %(total)s'),
    'TOTAL_SUM_NOT_LESS_THAN_OR_EQUALS': lazy_gettext(
        'Enter answers that add up to or are less than %(total)s'
    ),
    'TOTAL_SUM_NOT_LESS_THAN': lazy_gettext(
        'Enter answers that add up to less than %(total)s'
    ),
    'TOTAL_SUM_NOT_GREATER_THAN': lazy_gettext(
        'Enter answers that add up to greater than %(total)s'
    ),
    'TOTAL_SUM_NOT_GREATER_THAN_OR_EQUALS': lazy_gettext(
        'Enter answers that add up to or are greater than %(total)s'
    ),
    'INVALID_NUMBER': lazy_gettext('Enter a number.'),
    'INVALID_INTEGER': lazy_gettext('Enter a whole number.'),
    'INVALID_DECIMAL': lazy_gettext(
        'Enter a number rounded to %(max)d decimal places.'
    ),
    'MAX_LENGTH_EXCEEDED': lazy_gettext(
        'Your answer is too long, it has to be less than %(max)d characters.'
    ),
    'INVALID_DATE': lazy_gettext('Enter a valid date.'),
    'INVALID_DATE_RANGE': lazy_gettext(
        "Enter a 'period to' date later than the 'period from' date."
    ),
    'INVALID_DURATION': lazy_gettext('Enter a valid duration.'),
    'DATE_PERIOD_TOO_SMALL': lazy_gettext(
        'Enter a reporting period greater than or equal to %(min)s.'
    ),
    'DATE_PERIOD_TOO_LARGE': lazy_gettext(
        'Enter a reporting period less than or equal to %(max)s.'
    ),
    'SINGLE_DATE_PERIOD_TOO_EARLY': lazy_gettext('Enter a date after %(min)s.'),
    'SINGLE_DATE_PERIOD_TOO_LATE': lazy_gettext('Enter a date before %(max)s.'),
    'MUTUALLY_EXCLUSIVE': lazy_gettext('Remove an answer to continue.'),
}
