import re
from datetime import datetime
from decimal import Decimal, InvalidOperation

import flask_babel
from flask_babel import ngettext
from babel import numbers
from dateutil.relativedelta import relativedelta
from structlog import get_logger
from wtforms import validators
from wtforms.compat import string_types

from app.jinja_filters import format_number, get_formatted_currency
from app.questionnaire.rules import convert_to_datetime
from app.validation.error_messages import error_messages

logger = get_logger()


class NumberCheck:
    def __init__(self, message=None):
        if message:
            self.message = message
        else:
            self.message = error_messages['INVALID_NUMBER']

    def __call__(self, form, field):
        try:
            Decimal(field.raw_data[0].replace(numbers.get_group_symbol(flask_babel.get_locale()), ''))
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
        data = field.raw_data[0].replace(numbers.get_group_symbol(flask_babel.get_locale()), '').replace(' ', '')
        decimal_symbol = numbers.get_decimal_symbol(flask_babel.get_locale())
        if data and decimal_symbol in data:
            if self.max_decimals == 0:
                raise validators.ValidationError(self.messages['INVALID_INTEGER'])
            if len(data.split(decimal_symbol)[1]) > self.max_decimals:
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
            datetime.strptime(form.data, '%Y-%m-%d')
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
            raise validators.StopValidation(self.message)


class YearCheck:
    def __init__(self, message=None):
        self.message = message or error_messages['INVALID_DATE']

    def __call__(self, form, field):
        # Must be 4 digits long
        if not re.match(r'\d{4}$', str(form.year.data)):
            raise validators.StopValidation(self.message)


class SingleDatePeriodCheck:
    def __init__(self, messages=None, date_format='d MMMM YYYY', minimum_date=None, maximum_date=None):
        self.messages = messages or error_messages
        self.minimum_date = minimum_date
        self.maximum_date = maximum_date
        self.date_format = date_format

    def __call__(self, form, field):
        date = convert_to_datetime(form.data)

        if self.minimum_date:
            if date < self.minimum_date:
                raise validators.ValidationError(self.messages['SINGLE_DATE_PERIOD_TOO_EARLY'] %
                                                 dict(min=self._format_playback_date(self.minimum_date + relativedelta(days=-1),
                                                                                     self.date_format)))

        if self.maximum_date:
            if date > self.maximum_date:
                raise validators.ValidationError(self.messages['SINGLE_DATE_PERIOD_TOO_LATE'] %
                                                 dict(max=self._format_playback_date(self.maximum_date + relativedelta(days=+1),
                                                                                     self.date_format)))

    @staticmethod
    def _format_playback_date(date, date_format='d MMMM YYYY'):
        return flask_babel.format_date(date, format=date_format)


class DateRangeCheck:
    def __init__(self, messages=None, period_min=None, period_max=None):
        self.messages = messages or error_messages
        self.period_min = period_min
        self.period_max = period_max

    def __call__(self, form, from_field, to_field):
        from_date = convert_to_datetime(from_field.data)
        to_date = convert_to_datetime(to_field.data)

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

    @staticmethod
    def _build_range_length_error(period_object):
        error_message = ''
        if 'years' in period_object:
            error_message = ngettext('%(num)s year', '%(num)s years', period_object['years'])
        if 'months' in period_object:
            message_addition = ngettext('%(num)s month', '%(num)s months', period_object['months'])
            error_message += message_addition if error_message == '' else ', ' + message_addition
        if 'days' in period_object:
            message_addition = ngettext('%(num)s day', '%(num)s days', period_object['days'])
            error_message += message_addition if error_message == '' else ', ' + message_addition

        return error_message


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
        if condition == 'less than':
            return total < target_total, 'TOTAL_SUM_NOT_LESS_THAN'
        if condition == 'greater than':
            return total > target_total, 'TOTAL_SUM_NOT_GREATER_THAN'
        if condition == 'greater than or equals':
            return total >= target_total, 'TOTAL_SUM_NOT_GREATER_THAN_OR_EQUALS'
        if condition == 'less than or equals':
            return total <= target_total, 'TOTAL_SUM_NOT_LESS_THAN_OR_EQUALS'


def format_playback_value(value, currency=None):
    if currency:
        return get_formatted_currency(value, currency)
    return format_number(value)


class MutuallyExclusiveCheck:
    def __init__(self, messages=None):
        self.messages = messages or error_messages

    def __call__(self, answer_values, is_mandatory):
        total_answered = sum(1 for value in answer_values if value)
        if total_answered > 1:
            raise validators.ValidationError(self.messages['MUTUALLY_EXCLUSIVE'])
        if is_mandatory and total_answered < 1:
            raise validators.ValidationError(self.messages['MANDATORY_QUESTION'])
