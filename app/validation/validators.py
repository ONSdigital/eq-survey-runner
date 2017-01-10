from datetime import datetime

from app.validation.error_messages import error_messages

from wtforms import validators


def positive_integer_type_check(form, field):
    try:
        integer_value = int(field.data)  # NOQA
        if integer_value < 0:
            raise validators.ValidationError(error_messages['NEGATIVE_INTEGER'])
        if integer_value > 9999999999:  # 10 digits
            raise validators.ValidationError(error_messages['INTEGER_TOO_LARGE'])
    except (ValueError, TypeError):
        raise validators.ValidationError(error_messages['NOT_INTEGER'])


def date_check(form, field):

    try:
        date_str = "{:02d}/{:02d}/{}".format(int(form.day.data or 0), int(form.month.data or 0), form.year.data or '')

        datetime.strptime(date_str, "%d/%m/%Y")
    except ValueError:
        raise validators.ValidationError(error_messages['INVALID_DATE'])


def month_year_check(form, field):

    try:
        datestr = "{:02d}/{}".format(int(form.month.data or 0), form.year.data or '')

        datetime.strptime(datestr, "%m/%Y")
    except ValueError:
        raise validators.ValidationError(error_messages['INVALID_DATE'])


class DateRangeCheck(object):
    def __init__(self, to_field_data=None):
        self.to_field_data = to_field_data

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
                raise validators.ValidationError(error_messages['INVALID_DATE_RANGE_TO_FROM_SAME'])
            elif date_diff.total_seconds() < 0:
                raise validators.ValidationError(error_messages['INVALID_DATE_RANGE_TO_BEFORE_FROM'])
