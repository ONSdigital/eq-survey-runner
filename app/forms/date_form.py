import logging

from datetime import datetime
from enum import Enum

from dateutil.relativedelta import relativedelta

from wtforms import Form, StringField, FormField

from app.questionnaire.rules import (
    get_metadata_value,
    convert_to_datetime,
    get_answer_value,
)
from app.validation.validators import (
    DateCheck,
    OptionalForm,
    DateRequired,
    SingleDatePeriodCheck,
)
from app.utilities.schema import load_schema_from_metadata

logger = logging.getLogger(__name__)


class DateFormType(Enum):
    YearMonthDay = {'date_format': 'yyyy-mm-dd'}
    YearMonth = {'date_format': 'yyyy-mm'}
    Year = {'date_format': 'yyyy'}


class DateField(FormField):
    def __init__(
        self,
        date_form_type: DateFormType,
        answer_store,
        metadata,
        answer,
        error_messages,
        **kwargs,
    ):
        form_class = get_form(
            date_form_type, answer, answer_store, metadata, error_messages
        )
        super().__init__(form_class, **kwargs)

    def process(self, formdata, data=None):
        if data is not None:
            substrings = data.split('-')
            if len(substrings) == 3:
                data = {
                    'year': substrings[0],
                    'month': substrings[1],
                    'day': substrings[2],
                }
            if len(substrings) == 2:
                data = {'year': substrings[0], 'month': substrings[1]}
            if len(substrings) == 1:
                data = {'year': substrings[0]}

        super().process(formdata, data)


class CachedProperty:
    """ A property that is only computed once per instance and then replaces
        itself with an ordinary attribute. Deleting the attribute resets the
        property.

        Source: https://github.com/bottlepy/bottle/commit/fa7733e075da0d790d809aa3d2f53071897e6f76
        """

    def __init__(self, func):
        self.__doc__ = getattr(func, '__doc__')
        self.func = func

    def __get__(self, obj, cls):
        if obj is None:
            return self
        value = obj.__dict__[self.func.__name__] = self.func(obj)
        return value


class DateForm(Form):
    @CachedProperty
    def data(self):
        data = super().data
        try:
            if all(k in data for k in ('day', 'month', 'year')):
                return '{year:04d}-{month:02d}-{day:02d}'.format(
                    year=int(data['year']),
                    month=int(data['month']),
                    day=int(data['day']),
                )

            if all(k in data for k in ('month', 'year')):
                return '{year:04d}-{month:02d}'.format(
                    year=int(data['year']), month=int(data['month'])
                )

            if 'year' in data and data['year']:
                return '{year:04d}'.format(year=int(data['year']))

        except (TypeError, ValueError):
            return None


def get_form(form_type, answer, answer_store, metadata, error_messages):
    validate_with = [OptionalForm()]

    if answer['mandatory'] is True:
        validate_with = validate_mandatory_date(error_messages, answer)

    error_message = get_bespoke_message(answer, 'INVALID_DATE')

    validate_with.append(DateCheck(error_message))

    if 'minimum' in answer or 'maximum' in answer:
        min_max_validation = validate_min_max_date(
            answer, answer_store, metadata, form_type.value['date_format']
        )
        validate_with.append(min_max_validation)

    class CustomDateForm(DateForm):
        pass

    if form_type in DateFormType:
        # Validation is only ever added to the 1 field that shows in all 3 variants
        # This is to prevent an error message for each input box
        CustomDateForm.year = StringField(validators=validate_with)

    if form_type in [DateFormType.YearMonth, DateFormType.YearMonthDay]:
        CustomDateForm.month = StringField()

    if form_type == DateFormType.YearMonthDay:
        CustomDateForm.day = StringField()

    return CustomDateForm


def validate_mandatory_date(error_messages, answer):
    error_message = (
        get_bespoke_message(answer, 'MANDATORY_DATE')
        or error_messages['MANDATORY_DATE']
    )

    validate_with = [DateRequired(message=error_message)]
    return validate_with


def get_bespoke_message(answer, message_type):
    if (
        'validation' in answer
        and 'messages' in answer['validation']
        and message_type in answer['validation']['messages']
    ):
        return answer['validation']['messages'][message_type]

    return None


def validate_min_max_date(answer, answer_store, metadata, date_format):
    messages = None
    if 'validation' in answer:
        messages = answer['validation'].get('messages')
    minimum_date, maximum_date = get_dates_for_single_date_period_validation(
        answer, answer_store, metadata
    )

    display_format = 'd MMMM yyyy'
    if date_format == 'yyyy-mm':
        display_format = 'MMMM yyyy'
        minimum_date = (
            minimum_date.replace(day=1) if minimum_date else None
        )  # First day of Month
        maximum_date = (
            maximum_date + relativedelta(day=31) if maximum_date else None
        )  # Last day of month
    elif date_format == 'yyyy':
        display_format = 'yyyy'
        minimum_date = (
            minimum_date.replace(month=1, day=1) if minimum_date else None
        )  # January 1st
        maximum_date = (
            maximum_date.replace(month=12, day=31) if maximum_date else None
        )  # Last day of december

    return SingleDatePeriodCheck(
        messages=messages,
        date_format=display_format,
        minimum_date=minimum_date,
        maximum_date=maximum_date,
    )


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
        minimum_referenced_date = get_referenced_offset_value(
            answer['minimum'], answer_store, metadata
        )
    if 'maximum' in answer:
        maximum_referenced_date = get_referenced_offset_value(
            answer['maximum'], answer_store, metadata
        )

    # Extra runtime validation that will catch invalid schemas
    # Similar validation in schema validator
    if minimum_referenced_date and maximum_referenced_date:
        if minimum_referenced_date > maximum_referenced_date:
            raise Exception(
                'The minimum offset date is greater than the maximum offset date for {}.'.format(
                    answer['id']
                )
            )

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
        schema = load_schema_from_metadata(metadata)
        answer_id = answer_min_or_max['answer_id']
        value = get_answer_value(answer_id, answer_store, schema)

    value = convert_to_datetime(value)

    if 'offset_by' in answer_min_or_max:
        offset = answer_min_or_max['offset_by']
        value += relativedelta(
            years=offset.get('years', 0),
            months=offset.get('months', 0),
            days=offset.get('days', 0),
        )

    return value
