import logging

from datetime import datetime

from dateutil.relativedelta import relativedelta

from wtforms import Form, SelectField, StringField
from flask_babel import gettext as _
from babel.dates import get_month_names

from app.settings import BABEL_DEFAULT_LOCALE
from app.forms.custom_fields import CustomIntegerField
from app.questionnaire.rules import get_metadata_value, get_answer_store_value, convert_to_datetime
from app.validation.validators import DateCheck, OptionalForm, DateRequired, MonthYearCheck, YearCheck, SingleDatePeriodCheck

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

    if answer['mandatory'] is True:
        validate_with = validate_mandatory_date(error_messages, answer)

    error_message = get_bespoke_message(answer, 'INVALID_DATE') or error_messages['INVALID_DATE']

    validate_with.append(DateCheck(error_message))

    if 'minimum' in answer or 'maximum' in answer:
        min_max_validation = validate_min_max_date(answer, answer_store, metadata, 'yyyy-mm-dd')
        validate_with.append(min_max_validation)

    # Set up all the calendar month choices for select
    DateForm.month = get_month_selection_field(validate_with)

    return DateForm


def get_month_year_form(answer, answer_store, metadata, error_messages):
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
        validate_with = validate_mandatory_date(error_messages, answer)

    error_message = get_bespoke_message(answer, 'INVALID_DATE')
    validate_with.append(MonthYearCheck(error_message))

    if 'minimum' in answer or 'maximum' in answer:
        min_max_validation = validate_min_max_date(answer, answer_store, metadata, 'yyyy-mm')
        validate_with.append(min_max_validation)

    MonthYearDateForm.month = get_month_selection_field(validate_with)

    return MonthYearDateForm


def get_year_form(answer, answer_store, metadata, error_messages, label, guidance):
    """
    Returns a year form metaclass with appropriate validators. Used in both date and
    date range form creation.

    :param answer: The answer on which to base this form
    :param error_messages: The messages to use upon this form during validation
    :return: The generated MonthYearDateForm metaclass
    """

    class YearDateForm(Form):
        year = None

    validate_with = [OptionalForm()]

    if answer['mandatory'] is True:
        validate_with = validate_mandatory_date(error_messages, answer)

    error_message = get_bespoke_message(answer, 'INVALID_DATE')
    validate_with.append(YearCheck(error_message))

    if 'minimum' in answer or 'maximum' in answer:
        min_max_validation = validate_min_max_date(answer, answer_store, metadata, 'yyyy')
        validate_with.append(min_max_validation)

    YearDateForm.year = CustomIntegerField(
        label=label,
        validators=validate_with,
        description=guidance,
    )

    return YearDateForm


def validate_mandatory_date(error_messages, answer):
    error_message = get_bespoke_message(answer, 'MANDATORY_DATE') or error_messages['MANDATORY_DATE']

    validate_with = [DateRequired(message=error_message)]
    return validate_with


def get_bespoke_message(answer, message_type):
    if ('validation' in answer and 'messages' in answer['validation'] and
            message_type in answer['validation']['messages']):
        return answer['validation']['messages'][message_type]

    return None


def get_month_selection_field(validate_with):
    month_names = get_month_names(locale=BABEL_DEFAULT_LOCALE)._data
    month_choices = [('', _('Select month'))] + [(str(key), month_names[key]) for key in range(1, 13)]
    return SelectField(choices=month_choices, default='', validators=validate_with)


def validate_min_max_date(answer, answer_store, metadata, date_format):
    messages = None
    if 'validation' in answer:
        messages = answer['validation'].get('messages')
    minimum_date, maximum_date = get_dates_for_single_date_period_validation(answer, answer_store, metadata)

    display_format = '%-d %B %Y'
    if date_format == 'yyyy-mm':
        display_format = '%B %Y'
        minimum_date = minimum_date.replace(day=1) if minimum_date else None    # First day of Month
        maximum_date = maximum_date + relativedelta(day=31) if maximum_date else None   # Last day of month
    elif date_format == 'yyyy':
        display_format = '%Y'
        minimum_date = minimum_date.replace(month=1, day=1) if minimum_date else None    # January 1st
        maximum_date = maximum_date.replace(month=12, day=31) if maximum_date else None   # Last day of december

    return SingleDatePeriodCheck(messages=messages, date_format=display_format, minimum_date=minimum_date, maximum_date=maximum_date)


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
