import logging
import calendar

from wtforms import Form, SelectField, StringField

from app.validation.validators import DateCheck, OptionalForm, DateRequired, MonthYearCheck

logger = logging.getLogger(__name__)


def get_date_form(answer=None, error_messages=None):
    """
    Returns a date form metaclass with appropriate validators. Used in both date and
    date range form creation.

    :param error_messages: The messages during validation
    :param answer: The answer on which to base this form
    :return: The generated DateForm metaclass
    """
    class DateForm(Form):
        day = StringField()
        year = StringField()

    validate_with = [OptionalForm()]

    if not error_messages:
        date_messages = {}
    else:
        date_messages = error_messages.copy()

    if answer['mandatory'] is True:
        if 'validation' in answer and 'messages' in answer['validation'] \
                and 'MANDATORY' in answer['validation']['messages']:
            date_messages['MANDATORY'] = answer['validation']['messages']['MANDATORY']

        validate_with = [DateRequired(message=date_messages['MANDATORY'])]

    if 'validation' in answer and 'messages' in answer['validation'] \
            and 'INVALID_DATE' in answer['validation']['messages']:
        date_messages['INVALID_DATE'] = answer['validation']['messages']['INVALID_DATE']

    validate_with += [DateCheck(date_messages['INVALID_DATE'])]

    # Set up all the calendar month choices for select
    month_choices = [('', 'Select month')] + [(str(x), calendar.month_name[x]) for x in range(1, 13)]

    DateForm.month = SelectField(choices=month_choices, default='', validators=validate_with)

    return DateForm


def get_month_year_form(answer, error_messages):
    """
    Returns a month year form metaclass with appropriate validators. Used in both date and
    date range form creation.

    :param answer: The answer on which to base this form
    :param error_messages: The messages to use upon this form during validation
    :return: The generated MonthYearDateForm metaclass
    """
    class MonthYearDateForm(Form):
        year = StringField()

    validate_with = [OptionalForm()]

    if answer['mandatory'] is True:
        error_message = error_messages['MANDATORY']
        if 'validation' in answer and 'messages' in answer['validation'] \
                and 'MANDATORY' in answer['validation']['messages']:
            error_message = answer['validation']['messages']['MANDATORY']

        validate_with = [DateRequired(message=error_message)]

    if 'validation' in answer and 'messages' in answer['validation'] \
            and 'INVALID_DATE' in answer['validation']['messages']:
        error_message = answer['validation']['messages']['INVALID_DATE']
        validate_with += [MonthYearCheck(error_message)]
    else:
        validate_with += [MonthYearCheck()]

    # Set up all the calendar month choices for select
    month_choices = [('', 'Select month')] + [(str(x), calendar.month_name[x]) for x in range(1, 13)]

    MonthYearDateForm.month = SelectField(choices=month_choices, default='', validators=validate_with)

    return MonthYearDateForm
