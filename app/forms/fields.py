from wtforms import FormField, IntegerField, SelectField, SelectMultipleField, StringField, TextAreaField
from wtforms import validators

from app.forms.date_form import get_date_form, get_month_year_form
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


def get_select_multiple_field(answer, label, guidance, error_messages):
    validate_with = get_mandatory_validator(answer, error_messages)

    return SelectMultipleField(
        label=label,
        description=guidance,
        choices=build_choices(answer['options']),
        validators=validate_with,
    )


def _coerce_str_unless_none(value):
    """
    Coerces a value using str() unless that value is None
    :param value: Any value that can be coerced using str() or None
    :return: str(value) or None if value is None
    """
    return str(value) if value is not None else None


def get_select_field(answer, label, guidance, error_messages):
    validate_with = get_mandatory_validator(answer, error_messages)

    # We use a custom coerce function to avoid a defect where Python NoneType
    # is coerced to the string 'None' which clashes with legitimate Radio field
    # values of 'None'; i.e. there is no way to differentiate between the user
    # not providing an answer and them selecting the 'None' option otherwise.
    # https://github.com/ONSdigital/eq-survey-runner/issues/1013
    # See related WTForms PR: https://github.com/wtforms/wtforms/pull/288

    return SelectField(
        label=label,
        description=guidance,
        choices=build_choices(answer['options']),
        validators=validate_with,
        coerce=_coerce_str_unless_none,
    )


class CustomIntegerField(IntegerField):
    """
    The default wtforms field coerces data to an int and raises
    cast errors outside of it's validation chain. In order to stop
    the validation chain, we create a custom field that doesn't
    raise the error and we can instead fail and stop other calls to
    further validation steps by using a separate IntegerCheck validator
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = None

    def process_formdata(self, valuelist):

        if valuelist:
            try:
                self.data = int(valuelist[0])
            except ValueError:
                pass


def get_integer_field(answer, label, guidance, error_messages):
    answer_errors = error_messages.copy()

    if 'validation' in answer and 'messages' in answer['validation']:
        for error_key, error_message in answer['validation']['messages'].items():
            answer_errors[error_key] = error_message

    mandatory_or_optional = get_mandatory_validator(answer, answer_errors)

    if answer['type'] == 'Integer':
        validate_with = mandatory_or_optional + [
            IntegerCheck(answer_errors['NOT_INTEGER']),
            NumberRange(maximum=9999999999, messages=answer_errors),
        ]
    elif answer['type'] == 'Percentage':
        validate_with = mandatory_or_optional + [
            IntegerCheck(answer_errors['NOT_INTEGER']),
            NumberRange(minimum=0, maximum=100, messages=answer_errors),
        ]
    else:
        validate_with = mandatory_or_optional + [
            IntegerCheck(answer_errors['NOT_INTEGER']),
            NumberRange(minimum=0, maximum=9999999999, messages=answer_errors),
        ]

    return CustomIntegerField(
        label=label,
        description=guidance,
        validators=validate_with,
    )
