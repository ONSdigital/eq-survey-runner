from flask_babel import gettext

# Set up default error and warning messages
error_messages = {
    'MANDATORY_QUESTION': gettext('Enter an answer to continue.'),
    'MANDATORY_TEXTFIELD': gettext('Enter an answer to continue.'),
    'MANDATORY_NUMBER': gettext('Enter an answer to continue.'),
    'MANDATORY_TEXTAREA': gettext('Enter an answer to continue.'),
    'MANDATORY_RADIO': gettext('Select an answer to continue.'),
    'MANDATORY_DROPDOWN': gettext('Select an answer to continue.'),
    'MANDATORY_CHECKBOX': gettext('Select all that apply to continue.'),
    'MANDATORY_DATE': gettext('Enter a date to continue.'),
    'MANDATORY_DURATION': gettext('Enter a duration to continue.'),
    'NUMBER_TOO_SMALL': gettext('Enter an answer more than or equal to %(min)s.'),
    'NUMBER_TOO_LARGE': gettext('Enter an answer less than or equal to %(max)s.'),
    'NUMBER_TOO_SMALL_EXCLUSIVE': gettext('Enter an answer more than %(min)s.'),
    'NUMBER_TOO_LARGE_EXCLUSIVE': gettext('Enter an answer less than %(max)s.'),
    'TOTAL_SUM_NOT_EQUALS': gettext('Enter answers that add up to %(total)s'),
    'TOTAL_SUM_NOT_LESS_THAN_OR_EQUALS': gettext(
        'Enter answers that add up to or are less than %(total)s'
    ),
    'TOTAL_SUM_NOT_LESS_THAN': gettext(
        'Enter answers that add up to less than %(total)s'
    ),
    'TOTAL_SUM_NOT_GREATER_THAN': gettext(
        'Enter answers that add up to greater than %(total)s'
    ),
    'TOTAL_SUM_NOT_GREATER_THAN_OR_EQUALS': gettext(
        'Enter answers that add up to or are greater than %(total)s'
    ),
    'INVALID_NUMBER': gettext('Enter a number.'),
    'INVALID_INTEGER': gettext('Enter a whole number.'),
    'INVALID_DECIMAL': gettext('Enter a number rounded to %(max)d decimal places.'),
    'MAX_LENGTH_EXCEEDED': gettext(
        'Your answer is too long, it has to be less than %(max)d characters.'
    ),
    'INVALID_DATE': gettext('Enter a valid date.'),
    'INVALID_DATE_RANGE': gettext(
        "Enter a 'period to' date later than the 'period from' date."
    ),
    'INVALID_DURATION': gettext('Enter a valid duration.'),
    'DATE_PERIOD_TOO_SMALL': gettext(
        'Enter a reporting period greater than or equal to %(min)s.'
    ),
    'DATE_PERIOD_TOO_LARGE': gettext(
        'Enter a reporting period less than or equal to %(max)s.'
    ),
    'SINGLE_DATE_PERIOD_TOO_EARLY': gettext('Enter a date after %(min)s.'),
    'SINGLE_DATE_PERIOD_TOO_LATE': gettext('Enter a date before %(max)s.'),
    'MUTUALLY_EXCLUSIVE': gettext('Remove an answer to continue.'),
}
