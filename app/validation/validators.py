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


def date_range_check(form, field):
    try:

        if form.date_from and form.date_to:
            from_date = datetime.strptime(form.date_from, "%d/%m/%Y")
            to_date = datetime.strptime(form.date_to, "%d/%m/%Y")
            date_diff = to_date - from_date

            if date_diff.total_seconds() == 0:
                raise validators.ValidationError(error_messages['INVALID_DATE_RANGE_TO_FROM_SAME'])
            elif date_diff.total_seconds() < 0:
                raise validators.ValidationError(error_messages['INVALID_DATE_RANGE_TO_BEFORE_FROM'])

    except (ValueError, TypeError, AttributeError):
        raise validators.ValidationError(error_messages['INVALID_DATE'])
