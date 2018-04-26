import logging
import calendar

from datetime import datetime

from dateutil.relativedelta import relativedelta

from wtforms import Form, SelectField, StringField

from app.questionnaire.rules import get_metadata_value, get_answer_store_value, convert_to_datetime
from app.validation.validators import DateCheck, OptionalForm, DateRequired, MonthYearCheck, SingleDatePeriodCheck

logger = logging.getLogger(__name__)


def get_date_form(answer_store, metadata, answer=None, error_messages=None):
    """
    Returns a date form metaclass with appropriate validators. Used in both date and
    date range form creation.

    :param error_messages: The messages during validation
    :param answer: The answer on which to base this form
    :param answer_store: The current answer store
    :param metadata: metadata for reference meta dates
    :return: The generated DateForm metaclass
    """
    class DateForm(Form):
        day = StringField()
        year = StringField()

    validate_with = [OptionalForm()]

    if error_messages:
        date_messages = error_messages.copy()
    else:
        date_messages = {}

    if answer['mandatory'] is True:
        if 'validation' in answer and 'messages' in answer['validation'] \
                and 'MANDATORY_DATE' in answer['validation']['messages']:
            date_messages['MANDATORY_DATE'] = answer['validation']['messages']['MANDATORY_DATE']

        validate_with = [DateRequired(message=date_messages['MANDATORY_DATE'])]

    if 'validation' in answer and 'messages' in answer['validation'] \
            and 'INVALID_DATE' in answer['validation']['messages']:
        date_messages['INVALID_DATE'] = answer['validation']['messages']['INVALID_DATE']

    validate_with.append(DateCheck(date_messages['INVALID_DATE']))

    if 'minimum' in answer or 'maximum' in answer:
        messages = None
        if 'validation' in answer:
            messages = answer['validation'].get('messages')
        minimum_date, maximum_date = get_dates_for_single_date_period_validation(answer, answer_store, metadata)
        validate_with.append(SingleDatePeriodCheck(messages=messages, minimum_date=minimum_date, maximum_date=maximum_date))

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
        error_message = error_messages['MANDATORY_DATE']
        if 'validation' in answer and 'messages' in answer['validation'] \
                and 'MANDATORY_DATE' in answer['validation']['messages']:
            error_message = answer['validation']['messages']['MANDATORY_DATE']

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


def get_dates_for_single_date_period_validation(answer, answer_store, metadata):
    """
    Gets attributes within a minimum or maximum of a date field and validates that the entered date
    is valid.

    :param answer: The answer which contains the minimum or maximum
    :param answer_store: The current answer store
    :param metadata: metadata for reference meta dates
    :return: attributes
    """
    minimum_referenced_date, maximum_referenced_date = None, None

    if 'minimum' in answer:
        minimum_referenced_date = get_referenced_offset_value(answer['minimum'], answer_store, metadata)
    if 'maximum' in answer:
        maximum_referenced_date = get_referenced_offset_value(answer['maximum'], answer_store, metadata)

    # Extra runtime validation that will catch invalid schemas
    # Similar validation in schema validator
    if minimum_referenced_date and maximum_referenced_date:
        if minimum_referenced_date > maximum_referenced_date:
            raise Exception('The minimum offset date is greater than the maximum offset date for {}.'.format(answer['id']))

    return minimum_referenced_date, maximum_referenced_date


def get_referenced_offset_value(answer_min_or_max, answer_store, metadata):
    """
    Gets value of the referenced date type, whether it is a value,
    id of an answer or a meta date. Then adds/subtracts offset from that value and returns
    the new offset value

    :param answer_min_or_max: The minimum or maximum object which contains
    the referenced value.
    :param answer_store: The current answer store
    :param metadata: metadata for reference meta dates
    :return: date value
    """
    value = None

    if 'value' in answer_min_or_max:
        if answer_min_or_max['value'] == 'now':
            value = datetime.utcnow().strftime('%Y-%m-%d')
        else:
            value = answer_min_or_max['value']
    elif 'meta' in answer_min_or_max:
        value = get_metadata_value(metadata, answer_min_or_max['meta'])
    elif 'answer_id' in answer_min_or_max:
        value = get_answer_store_value(answer_min_or_max['answer_id'], answer_store, group_instance=0)

    value = convert_to_datetime(value)

    if 'offset_by' in answer_min_or_max:
        offset = answer_min_or_max['offset_by']
        value += relativedelta(years=offset.get('years', 0),
                               months=offset.get('months', 0),
                               days=offset.get('days', 0))

    return value
