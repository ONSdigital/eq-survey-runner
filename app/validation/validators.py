from datetime import datetime

from app.validation.error_messages import error_messages

from wtforms import validators


class IntegerCheck(object):
    def __init__(self, messages=None):
        if not messages:
            messages = error_messages
        self.messages = messages

    def __call__(self, form, field):
        if len(field.raw_data) == 1:
            try:
                int(field.raw_data[0])
            except ValueError:
                raise validators.ValidationError(self.messages['NOT_INTEGER'])


class PositiveIntegerCheck(object):
    def __init__(self, messages=None):
        if not messages:
            messages = error_messages
        self.messages = messages

    def __call__(self, form, field):
        data = field.data
        if data is not None:
            if data < 0:
                raise validators.ValidationError(self.messages['NEGATIVE_INTEGER'])


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


class DateRequired(object):
    def __init__(self, message=None):
        if not message:
            message = error_messages['MANDATORY']
        self.message = message

    def __call__(self, form, field):
        if hasattr(form, 'day') and not (form.day.data and form.month.data and form.year.data):
            raise validators.ValidationError(self.message)
        elif not form.month.data or not form.year.data:
            raise validators.ValidationError(self.message)


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
            raise validators.ValidationError(self.message)


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
