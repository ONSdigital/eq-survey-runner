from decimal import Decimal, InvalidOperation
from datetime import datetime

from babel import numbers

from app.jinja_filters import format_number, format_currency
from app.settings import DEFAULT_LOCALE
from app.validation.error_messages import error_messages

from wtforms import validators
from wtforms.compat import string_types

from structlog import get_logger

logger = get_logger()


class NumberCheck(object):
    def __init__(self, message=None):
        if not message:
            message = error_messages['INVALID_NUMBER']
        self.message = message

    def __call__(self, form, field):
        try:
            Decimal(field.raw_data[0].replace(numbers.get_group_symbol(DEFAULT_LOCALE), ''))
        except (ValueError, TypeError, InvalidOperation, AttributeError):
            raise validators.StopValidation(self.message)

        if 'e' in field.raw_data[0].lower():
            raise validators.StopValidation(self.message)


class ResponseRequired(object):
    """
    Validates that input was provided for this field. This is a copy of the
    InputRequired validator provided by wtforms, which checks that form-input data
    was provided, but additionally adds a kwarg to strip whitespace, as is available
    on the Optional() validator wtforms provides. Oddly, stripping whitespace is not
    an option for DataRequired or InputRequired validators in wtforms.
    """
    field_flags = ('required', )

    def __init__(self, message, strip_whitespace=True):
        self.message = message

        if strip_whitespace:
            self.string_check = lambda s: s.strip()
        else:
            self.string_check = lambda s: s

    def __call__(self, form, field):
        if not field.raw_data or not field.raw_data[0] or not self.string_check(field.raw_data[0]):
            field.errors[:] = []
            raise validators.StopValidation(self.message)


class NumberRange(object):
    """
    Validates that a number is of a minimum and/or maximum value, inclusive.
    This will work with any comparable number type, such as floats and
    decimals, not just integers.

    :param minimum:
        The minimum required value of the number. If not provided, minimum
        value will not be checked.
    :param maximum:
        The maximum value of the number. If not provided, maximum value
        will not be checked.
    """
    def __init__(self, minimum=None, minimum_exclusive=False,
                 maximum=None, maximum_exclusive=False,
                 messages=None, currency=None):
        self.minimum = minimum
        self.maximum = maximum
        self.minimum_exclusive = minimum_exclusive
        self.maximum_exclusive = maximum_exclusive
        if not messages:
            messages = error_messages
        self.messages = messages
        self.currency = currency

    def __call__(self, form, field):
        value = field.data
        error_message = None
        if value is not None:
            if self.minimum is not None:
                error_message = self.validate_minimum(value)
            if error_message is None and self.maximum is not None:
                error_message = self.validate_maximum(value)

            if error_message:
                raise validators.ValidationError(error_message)

    def validate_minimum(self, value):
        if self.minimum_exclusive:
            if value <= self.minimum:
                return self.messages['NUMBER_TOO_SMALL_EXCLUSIVE'] % dict(min=self.format_min_max(self.minimum))
        else:
            if value < self.minimum:
                return self.messages['NUMBER_TOO_SMALL'] % dict(min=self.format_min_max(self.minimum))

        return None

    def validate_maximum(self, value):
        if self.maximum_exclusive:
            if value >= self.maximum:
                return self.messages['NUMBER_TOO_LARGE_EXCLUSIVE'] % dict(max=self.format_min_max(self.maximum))
        else:
            if value > self.maximum:
                return self.messages['NUMBER_TOO_LARGE'] % dict(max=self.format_min_max(self.maximum))

        return None

    def format_min_max(self, value):
        if self.currency:
            return format_currency(value, self.currency)
        return format_number(value)


class DecimalPlaces(object):
    """
    Validates that an input has less than or equal to a
    set number of decimal places

    :param max_decimals:
        The maximum allowed number of decimal places.
    """
    def __init__(self, max_decimals=0, messages=None):
        self.max_decimals = max_decimals
        if not messages:
            messages = error_messages
        self.messages = messages

    def __call__(self, form, field):
        data = field.raw_data[0].replace(numbers.get_group_symbol(DEFAULT_LOCALE), '')
        decimal_symbol = numbers.get_decimal_symbol(DEFAULT_LOCALE)
        if data and decimal_symbol in data:
            if self.max_decimals == 0:
                raise validators.ValidationError(self.messages['INVALID_INTEGER'])
            elif len(data.split(decimal_symbol)[1]) > self.max_decimals:
                raise validators.ValidationError(self.messages['INVALID_DECIMAL'] % dict(max=self.max_decimals))


class OptionalForm(object):
    """
    Allows completely empty form and stops the validation chain from continuing.
    Will not stop the validation chain if any one of the fields is populated.
    """
    field_flags = ('optional',)

    def __call__(self, form, field):
        empty_form = True

        for formfield in form:
            has_raw_data = hasattr(formfield, 'raw_data')

            is_empty = has_raw_data and len(formfield.raw_data) == 0
            is_blank = has_raw_data and len(formfield.raw_data) >= 1 \
                and isinstance(formfield.raw_data[0], string_types) and not formfield.raw_data[0]

            # By default we'll receive empty arrays for values not posted, so need to allow empty lists
            empty_field = True if is_empty else is_blank

            empty_form &= empty_field

        if empty_form:
            raise validators.StopValidation()


class DateRequired(object):
    field_flags = ('required', )

    def __init__(self, message=None):
        if not message:
            message = error_messages['MANDATORY_DATE']
        self.message = message

    def __call__(self, form, field):
        if hasattr(form, 'day'):
            if not form.day.data and not form.month.data and not form.year.data:
                raise validators.StopValidation(self.message)
        else:
            if not form.month.data and not form.year.data:
                raise validators.StopValidation(self.message)


class DateCheck(object):
    def __init__(self, message=None):
        if not message:
            message = error_messages['INVALID_DATE']
        self.message = message

    def __call__(self, form, field):
        try:
            date_str = '{}-{:02d}-{:02d}'.format(int(form.year.data or 0),
                                                 int(form.month.data or 0),
                                                 int(form.day.data or 0))

            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            raise validators.StopValidation(self.message)


class MonthYearCheck(object):
    def __init__(self, message=None):
        if not message:
            message = error_messages['INVALID_DATE']
        self.message = message

    def __call__(self, form, field):
        try:
            datestr = '{}-{:02d}'.format(int(form.year.data or 0), int(form.month.data or 0))

            datetime.strptime(datestr, '%Y-%m')
        except ValueError:
            raise validators.ValidationError(self.message)


class DateRangeCheck(object):
    def __init__(self, messages=None):
        if not messages:
            messages = error_messages
        self.messages = messages

    def __call__(self, form, from_field, to_field):

        from_date_str = '{}-{:02d}-{:02d}'.format(int(from_field.year.data or 0),
                                                  int(from_field.month.data or 0),
                                                  int(from_field.day.data or 0))

        to_date_str = '{}-{:02d}-{:02d}'.format(int(to_field.year.data or 0),
                                                int(to_field.month.data or 0),
                                                int(to_field.day.data or 0))

        from_date = datetime.strptime(from_date_str, '%Y-%m-%d')
        to_date = datetime.strptime(to_date_str, '%Y-%m-%d')

        if from_date == to_date or from_date > to_date:
            raise validators.ValidationError(self.messages['INVALID_DATE_RANGE'])
