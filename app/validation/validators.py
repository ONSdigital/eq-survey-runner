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


class ResponseRequired(object):
    """
    Validates that input was provided for this field. This is a copy of the
    InputRequired validator provided by wtforms, which checks that form-input data
    was provided, but additionally adds a kwarg to strip whitespace, as is available
    on the Optional() validator wtforms provides. Oddly, stripping whitespace is not
    an option for DataRequired or InputRequired validators in wtforms.
    """
    field_flags = ('required', )

    def __init__(self, message=None, strip_whitespace=True):
        if not message:
            message = error_messages['MANDATORY']
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
    def __init__(self, minimum=None, maximum=None, messages=None):
        self.minimum = minimum
        self.maximum = maximum
        if not messages:
            messages = error_messages
        self.messages = messages

    def __call__(self, form, field):
        data = field.data
        if data is not None:
            if self.minimum is not None and data < self.minimum:
                raise validators.ValidationError(self.messages['NEGATIVE_INTEGER'])
            elif self.maximum is not None and data > self.maximum:
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
    def __init__(self, messages=None):
        if not messages:
            messages = error_messages
        self.messages = messages

    def __call__(self, form, from_field, to_field):

        from_date_str = "{:02d}/{:02d}/{}".format(int(from_field.day.data or 0), int(from_field.month.data or 0),
                                                  from_field.year.data or '')
        to_date_str = "{:02d}/{:02d}/{}".format(int(to_field.day.data or 0), int(to_field.month.data or 0),
                                                to_field.year.data or '')

        from_date = datetime.strptime(from_date_str, "%d/%m/%Y")
        to_date = datetime.strptime(to_date_str, "%d/%m/%Y")

        if from_date == to_date:
            raise validators.ValidationError(self.messages['INVALID_DATE_RANGE_TO_FROM_SAME'])
        elif from_date > to_date:
            raise validators.ValidationError(self.messages['INVALID_DATE_RANGE_TO_BEFORE_FROM'])
