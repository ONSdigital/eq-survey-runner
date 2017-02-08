from datetime import datetime

from app.validation.error_messages import error_messages

from wtforms import validators
from wtforms.compat import string_types


class IntegerCheck(object):
    def __init__(self, message=None):
        if not message:
            message = error_messages['NOT_INTEGER']
        self.message = message

    def __call__(self, form, field):
        try:
            int(field.raw_data[0])
        except (ValueError, TypeError):
            raise validators.StopValidation(self.message)


class NumberRange(object):
    """
    Validates that a number is of a minimum and/or maximum value, inclusive.
    This will work with any comparable number type, such as floats and
    decimals, not just integers.

    :param min:
        The minimum required value of the number. If not provided, minimum
        value will not be checked.
    :param max:
        The maximum value of the number. If not provided, maximum value
        will not be checked.
    """
    def __init__(self, min=None, max=None, messages=None):
        self.min = min
        self.max = max
        if not messages:
            messages = error_messages
        self.messages = messages

    def __call__(self, form, field):
        data = field.data
        if data is not None:
            if self.min is not None and data < self.min:
                raise validators.ValidationError(self.messages['NEGATIVE_INTEGER'])
            elif self.max is not None and data > self.max:
                raise validators.ValidationError(self.messages['INTEGER_TOO_LARGE'])


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
            message = error_messages['MANDATORY']
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
            date_str = "{:02d}/{:02d}/{}".format(int(form.day.data or 0), int(form.month.data or 0), form.year.data or '')

            datetime.strptime(date_str, "%d/%m/%Y")
        except ValueError:
            raise validators.StopValidation(self.message)


class MonthYearCheck(object):
    def __init__(self, message=None):
        if not message:
            message = error_messages['INVALID_DATE']
        self.message = message

    def __call__(self, form, field):
        try:
            datestr = "{:02d}/{}".format(int(form.month.data or 0), form.year.data or '')

            datetime.strptime(datestr, "%m/%Y")
        except ValueError:
            raise validators.ValidationError(self.message)


class DateRangeCheck(object):
    def __init__(self, to_field_data=None, messages=None):
        self.to_field_data = to_field_data
        if not messages:
            messages = error_messages
        self.messages = messages

    def __call__(self, form, from_field):

        if form.day and form.month and form.year and self.to_field_data:
            to_date_str = "{:02d}/{:02d}/{}".format(int(self.to_field_data['day'] or 0), int(self.to_field_data['month'] or 0),
                                                    self.to_field_data['year'] or '')
            from_date_str = "{:02d}/{:02d}/{}".format(int(form.day.data or 0), int(form.month.data or 0),
                                                      form.year.data or '')

            from_date = datetime.strptime(from_date_str, "%d/%m/%Y")
            to_date = datetime.strptime(to_date_str, "%d/%m/%Y")

            date_diff = to_date - from_date

            if date_diff.total_seconds() == 0:
                raise validators.ValidationError(self.messages['INVALID_DATE_RANGE_TO_FROM_SAME'])
            elif date_diff.total_seconds() < 0:
                raise validators.ValidationError(self.messages['INVALID_DATE_RANGE_TO_BEFORE_FROM'])
