from decimal import Decimal, InvalidOperation
from datetime import datetime

import re
from babel import numbers
from flask_babel import ngettext, lazy_gettext as _
from dateutil.relativedelta import relativedelta
from wtforms import validators
from wtforms.compat import string_types
from structlog import get_logger

from app.jinja_filters import format_number, format_currency
from app.settings import DEFAULT_LOCALE
from app.validation.error_messages import error_messages
from app.questionnaire.rules import convert_to_datetime

logger = get_logger()


class NumberCheck:
    def __init__(self, message=None):
        if message:
            self.message = message
        else:
            self.message = error_messages['INVALID_NUMBER']

    def __call__(self, form, field):
        try:
            Decimal(field.raw_data[0].replace(numbers.get_group_symbol(DEFAULT_LOCALE), ''))
        except (ValueError, TypeError, InvalidOperation, AttributeError):
            raise validators.StopValidation(self.message)

        if 'e' in field.raw_data[0].lower():
            raise validators.StopValidation(self.message)


class ResponseRequired:
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


class NumberRange:
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
        self.messages = messages or error_messages
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
                return self.messages['NUMBER_TOO_SMALL_EXCLUSIVE'] % dict(min=format_playback_value(self.minimum,
                                                                                                    self.currency))
        else:
            if value < self.minimum:
                return self.messages['NUMBER_TOO_SMALL'] % dict(min=format_playback_value(self.minimum, self.currency))

        return None

    def validate_maximum(self, value):
        if self.maximum_exclusive:
            if value >= self.maximum:
                return self.messages['NUMBER_TOO_LARGE_EXCLUSIVE'] % dict(max=format_playback_value(self.maximum,
                                                                                                    self.currency))
        else:
            if value > self.maximum:
                return self.messages['NUMBER_TOO_LARGE'] % dict(max=format_playback_value(self.maximum, self.currency))

        return None


class DecimalPlaces:
    """
    Validates that an input has less than or equal to a
    set number of decimal places

    :param max_decimals:
        The maximum allowed number of decimal places.
    """
    def __init__(self, max_decimals=0, messages=None):
        self.max_decimals = max_decimals
        self.messages = messages or error_messages

    def __call__(self, form, field):
        data = field.raw_data[0].replace(numbers.get_group_symbol(DEFAULT_LOCALE), '').replace(' ', '')
        decimal_symbol = numbers.get_decimal_symbol(DEFAULT_LOCALE)
        if data and decimal_symbol in data:
            if self.max_decimals == 0:
                raise validators.ValidationError(self.messages['INVALID_INTEGER'])
            elif len(data.split(decimal_symbol)[1]) > self.max_decimals:
                raise validators.ValidationError(self.messages['INVALID_DECIMAL'] % dict(max=self.max_decimals))


class OptionalForm:
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


class DateRequired:
    field_flags = ('required', )

    def __init__(self, message=None):
        self.message = message or error_messages['MANDATORY_DATE']

    def __call__(self, form, field):
        """
        Raise exception if ALL fields have not been filled out.
        Not having that field is the same as not filling it out
        as the remaining fields would also have to be empty for
        exception to be raised.
        """
        day_not_entered = not form.day.data if hasattr(form, 'day') else True
        month_not_entered = not form.month.data if hasattr(form, 'month') else True
        year_not_entered = not form.year.data

        if day_not_entered and month_not_entered and year_not_entered:
            raise validators.StopValidation(self.message)


class DateCheck:
    def __init__(self, message=None):
        self.message = message or error_messages['INVALID_DATE']

    def __call__(self, form, field):
        try:
            date_str = format_date_string(form)
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            raise validators.StopValidation(self.message)


class MonthYearCheck:
    def __init__(self, message=None):
        self.message = message or error_messages['INVALID_DATE']

    def __call__(self, form, field):
        try:
            datestr = '{}-{:02d}'.format(int(form.year.data or 0), int(form.month.data or 0))

            datetime.strptime(datestr, '%Y-%m')
        except ValueError:
            raise validators.ValidationError(self.message)


class YearCheck:
    def __init__(self, message=None):
        self.message = message or error_messages['INVALID_DATE']

    def __call__(self, form, field):
        # Must be 4 digits long
        if not re.match(r'\d{4}$', str(form.year.data)):
            raise validators.ValidationError(self.message)


class SingleDatePeriodCheck:
    def __init__(self, messages=None, date_format='%-d %B %Y', minimum_date=None, maximum_date=None):
        self.messages = messages or error_messages
        self.minimum_date = minimum_date
        self.maximum_date = maximum_date
        self.date_format = date_format

    def __call__(self, form, field):
        date_str = format_date_string(form)
        date = convert_to_datetime(date_str)

        if self.minimum_date:
            if date < self.minimum_date:
                raise validators.ValidationError(self.messages['SINGLE_DATE_PERIOD_TOO_EARLY'] %
                                                 dict(min=self._format_playback_date(self.minimum_date +
                                                                                     relativedelta(days=-1),
                                                                                     self.date_format)))

        if self.maximum_date:
            if date > self.maximum_date:
                raise validators.ValidationError(self.messages['SINGLE_DATE_PERIOD_TOO_LATE'] %
                                                 dict(max=self._format_playback_date(self.maximum_date +
                                                                                     relativedelta(days=+1),
                                                                                     self.date_format)))

    @staticmethod
    def _format_playback_date(date, date_format='%-d %B %Y'):
        return date.strftime(date_format)


class DateRangeCheck:
    def __init__(self, messages=None, period_min=None, period_max=None):
        self.messages = messages or error_messages
        self.period_min = period_min
        self.period_max = period_max

    def __call__(self, form, from_field, to_field):
        from_date_str = format_date_string(from_field)
        to_date_str = format_date_string(to_field)

        from_date = convert_to_datetime(from_date_str)
        to_date = convert_to_datetime(to_date_str)

        if from_date >= to_date:
            raise validators.ValidationError(self.messages['INVALID_DATE_RANGE'])

        answered_range_relative = relativedelta(to_date, from_date)

        if self.period_min:
            min_range = self._return_relative_delta(self.period_min)
            if self._is_first_relative_delta_largest(min_range, answered_range_relative):
                raise validators.ValidationError(self.messages['DATE_PERIOD_TOO_SMALL'] % dict(
                    min=self._build_range_length_error(self.period_min)))

        if self.period_max:
            max_range = self._return_relative_delta(self.period_max)
            if self._is_first_relative_delta_largest(answered_range_relative, max_range):
                raise validators.ValidationError(self.messages['DATE_PERIOD_TOO_LARGE'] % dict(
                    max=self._build_range_length_error(self.period_max)))

    @staticmethod
    def _return_relative_delta(period_object):
        return relativedelta(years=period_object.get('years', 0),
                             months=period_object.get('months', 0),
                             days=period_object.get('days', 0))

    @staticmethod
    def _is_first_relative_delta_largest(relativedelta1, relativedelta2):
        epoch = datetime.min    # generic epoch for comparison purposes only
        date1 = epoch + relativedelta1
        date2 = epoch + relativedelta2
        return date1 > date2

    def _build_range_length_error(self, period_object):
        error_message = ''
        if 'years' in period_object:
            error_message = self.return_error_component(error_message, period_object['years'], ' year')
        if 'months' in period_object:
            error_message = self.return_error_component(error_message, period_object['months'], ' month')
        if 'days' in period_object:
            error_message = self.return_error_component(error_message, period_object['days'], ' day')

        return error_message

    @staticmethod
    def return_error_component(error_message, number, unit):
        _('year'), _('years'), _('month'), _('months'), _('day'), _('days')
        plural = unit + 's' if number > 1 else unit

        if error_message != '':
            error_message = error_message + ', '

        error_message = error_message + str(number) + _(plural)

        return _(error_message)


class SumCheck:
    def __init__(self, messages=None, currency=None):
        self.messages = messages or error_messages
        self.currency = currency

    def __call__(self, form, conditions, total, target_total):
        if len(conditions) > 1:
            try:
                conditions.remove('equals')
            except ValueError:
                raise Exception(
                    'There are multiple conditions, but equals is not one of them. '
                    'We only support <= and >=')

            condition = '{} or equals'.format(conditions[0])
        else:
            condition = conditions[0]

        is_valid, message = self._is_valid(condition, total, target_total)

        if not is_valid:
            raise validators.ValidationError(self.messages[message] %
                                             dict(total=format_playback_value(target_total, self.currency)))

    @staticmethod
    def _is_valid(condition, total, target_total):
        if condition == 'equals':
            return total == target_total, 'TOTAL_SUM_NOT_EQUALS'
        elif condition == 'less than':
            return total < target_total, 'TOTAL_SUM_NOT_LESS_THAN'
        elif condition == 'greater than':
            return total > target_total, 'TOTAL_SUM_NOT_GREATER_THAN'
        elif condition == 'greater than or equals':
            return total >= target_total, 'TOTAL_SUM_NOT_GREATER_THAN_OR_EQUALS'
        elif condition == 'less than or equals':
            return total <= target_total, 'TOTAL_SUM_NOT_LESS_THAN_OR_EQUALS'


def format_playback_value(value, currency=None):
    if currency:
        return format_currency(value, currency)
    return format_number(value)


def format_date_string(field):
    day = int(field.data.get('day', 1))
    month = int(field.data.get('month', 1))
    return '{}-{:02d}-{:02d}'.format(int(field.data['year']),
                                     month,
                                     day)


class MutuallyExclusive:
    def __init__(self, options, messages=None):
        self.exclusive_value = options[-1]['value']
        self.value_labels = self._get_value_labels(options)
        self.messages = messages or error_messages

    def __call__(self, form, field):
        values = field.data
        if len(values) > 1 and self.exclusive_value in values:
            non_exclusives = self._build_non_exclusives(values)
            raise validators.ValidationError(self.messages['MUTUALLY_EXCLUSIVE'] %
                                             dict(non_exclusives=non_exclusives,
                                                  exclusive=self.value_labels[self.exclusive_value]))

    def _build_non_exclusives(self, values):
        non_exclusive_values = [
            '"{}"'.format(self.value_labels[value])
            for value in values
            if value != self.exclusive_value
        ]
        if len(non_exclusive_values) == 1:
            return non_exclusive_values[0]

        return '{} {} {}'.format(', '.join(_(non_exclusive_values[:-1])), _('and'), _(non_exclusive_values[-1]))

    @staticmethod
    def _get_value_labels(options):
        return {
            option['value']: option['label'] for option in options
        }
