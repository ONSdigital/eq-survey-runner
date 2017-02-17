from wtforms import FormField, SelectField, SelectMultipleField, StringField, TextAreaField
from wtforms import validators

from app.forms.custom_integer_field import CustomIntegerField
from app.forms.date_form import get_date_form, get_month_year_form
from app.forms.time_input_form import get_time_input_form
from app.validation.validators import IntegerCheck, NumberRange, ResponseRequired
from structlog import get_logger


logger = get_logger()


def get_field(answer, label, error_messages):
    guidance = answer.get('guidance', '')

    field = {
        "Radio": get_select_field,
        "Checkbox": get_select_multiple_field,
        "Date": get_date_field,
        "MonthYearDate": get_month_year_field,
        "Currency": get_integer_field,
        "Integer": get_integer_field,
        "PositiveInteger": get_integer_field,
        "Percentage": get_integer_field,
        "TextArea": get_text_area_field,
        "TextField": get_string_field,
        "TimeInput": get_time_input_field,
    }[answer['type']](answer, label, guidance, error_messages)

    if field is None:
        logger.error("Unknown answer type used during form creation", type=answer['type'])

    return field


def build_choices(options):
    choices = []
    for option in options:
        choices.append((option['value'], option['label']))
    return choices


def get_mandatory_validator(answer, error_messages):
    validate_with = [validators.Optional()]

    if answer['mandatory'] is True:
        mandatory_message = error_messages['MANDATORY']

        if 'validation' in answer and 'messages' in answer['validation'] \
                and 'MANDATORY' in answer['validation']['messages']:
            mandatory_message = answer['validation']['messages']['MANDATORY']

        validate_with = [
            ResponseRequired(
                message=mandatory_message,
            ),
        ]
    return validate_with


def get_string_field(answer, label, guidance, error_messages):
    validate_with = get_mandatory_validator(answer, error_messages)

    return StringField(
        label=label,
        description=guidance,
        validators=validate_with,
    )


def get_text_area_field(answer, label, guidance, error_messages):
    validate_with = get_mandatory_validator(answer, error_messages)

    return TextAreaField(
        label=label,
        description=guidance,
        validators=validate_with,
    )


def get_date_field(answer, label, guidance, error_messages):

    return FormField(
        get_date_form(answer, error_messages=error_messages),
        label=label,
        description=guidance,
    )


def get_month_year_field(answer, label, guidance, error_messages):
    return FormField(
        get_month_year_form(answer, error_messages),
        label=label,
        description=guidance,
    )


def get_time_input_field(answer, label, guidance, error_messages):
    return FormField(
        get_time_input_form(answer, error_messages),
        label=label,
        description=guidance,
    )


def get_select_multiple_field(answer, label, guidance, error_messages):
    validate_with = get_mandatory_validator(answer, error_messages)

    return SelectMultipleField(
        label=label,
        description=guidance,
        choices=build_choices(answer['options']),
        validators=validate_with,
    )


def get_select_field(answer, label, guidance, error_messages):
    validate_with = get_mandatory_validator(answer, error_messages)

    return SelectField(
        label=label,
        description=guidance,
        choices=build_choices(answer['options']),
        validators=validate_with,
    )


def get_integer_field(answer, label, guidance, error_messages):
    answer_errors = error_messages.copy()

    if 'validation' in answer and 'messages' in answer['validation']:
        for error_key, error_message in answer['validation']['messages'].items():
            answer_errors[error_key] = error_message

    mandatory_or_optional = get_mandatory_validator(answer, answer_errors)

    if answer['type'] == 'Integer':
        validate_with = mandatory_or_optional + [
            IntegerCheck(answer_errors['NOT_INTEGER']),
            NumberRange(max=9999999999, messages=answer_errors),
        ]
    elif answer['type'] == 'Percentage':
        validate_with = mandatory_or_optional + [
            IntegerCheck(answer_errors['NOT_INTEGER']),
            NumberRange(min=0, max=100, messages=answer_errors),
        ]
    else:
        validate_with = mandatory_or_optional + [
            IntegerCheck(answer_errors['NOT_INTEGER']),
            NumberRange(min=0, max=9999999999, messages=answer_errors),
        ]
    return CustomIntegerField(
        label=label,
        description=guidance,
        validators=validate_with,
    )
