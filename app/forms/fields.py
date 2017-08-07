from decimal import Decimal

from wtforms import FormField, SelectField, SelectMultipleField, StringField
from wtforms import validators

from app.forms.custom_fields import MaxTextAreaField, CustomIntegerField, CustomDecimalField
from app.forms.date_form import get_date_form, get_month_year_form
from app.validation.validators import NumberCheck, NumberRange, ResponseRequired, DecimalPlaces
from structlog import get_logger


MAX_LENGTH = 2000
MAX_NUMBER = 9999999999
MIN_NUMBER = -999999999
MAX_DECIMAL_PLACES = 6
logger = get_logger()


def get_field(answer, label, error_messages, answer_store):
    guidance = answer.get('guidance', '')

    if answer['type'] in ["Number", "Currency", "Percentage"]:
        field = get_number_field(answer, label, guidance, error_messages, answer_store)
    else:
        field = {
            "Radio": get_select_field,
            "Checkbox": get_select_multiple_field,
            "Date": get_date_field,
            "MonthYearDate": get_month_year_field,
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


def get_length_validator(answer, error_messages):
    validate_with = []
    max_length = MAX_LENGTH
    length_message = error_messages['MAX_LENGTH_EXCEEDED']

    if 'max_length' in answer and answer['max_length'] > 0:
        max_length = answer['max_length']

    if 'validation' in answer and 'messages' in answer['validation'] and \
            'MAX_LENGTH_EXCEEDED' in answer['validation']['messages']:
        length_message = answer['validation']['messages']['MAX_LENGTH_EXCEEDED']

    validate_with.append(
        validators.length(-1, max_length, message=length_message),
    )

    return validate_with


def get_mandatory_validator(answer, error_messages):
    validate_with = [validators.Optional()]

    if answer['mandatory'] is True:
        mandatory_message = error_messages['MANDATORY']

        if 'validation' in answer and 'messages' in answer['validation'] and \
                'MANDATORY' in answer['validation']['messages']:
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
    validate_with.extend(get_length_validator(answer, error_messages))

    return MaxTextAreaField(
        label=label,
        description=guidance,
        validators=validate_with,
        maxlength=MAX_LENGTH,
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


def get_number_field(answer, label, guidance, error_messages, answer_store):
    answer_errors = error_messages.copy()

    if 'validation' in answer and 'messages' in answer['validation']:
        for error_key, error_message in answer['validation']['messages'].items():
            answer_errors[error_key] = error_message

    mandatory_or_optional = get_mandatory_validator(answer, answer_errors)

    max_decimals = answer.get('decimal_places', 0)
    if max_decimals > MAX_DECIMAL_PLACES:
        raise Exception('decimal_places: {} > system maximum: {} for answer id: {}'
                        .format(max_decimals, MAX_DECIMAL_PLACES, answer['id']))

    min_value = get_schema_defined_limit(answer['id'], answer.get('min_value'), answer_store) or 0
    if min_value < MIN_NUMBER:
        raise Exception('min_value: {} < system minimum: {} for answer id: {}'
                        .format(min_value, MIN_NUMBER, answer['id']))

    max_value = get_schema_defined_limit(answer['id'], answer.get('max_value'), answer_store) or MAX_NUMBER
    if max_value > MAX_NUMBER:
        raise Exception('max_value: {} > system maximum: {} for answer id: {}'
                        .format(max_value, MAX_NUMBER, answer['id']))

    if min_value > max_value:
        raise Exception('min_value: {} > max_value: {} for answer id: {}'.format(min_value, max_value, answer['id']))

    validate_with = mandatory_or_optional + [
        NumberCheck(answer_errors['INVALID_NUMBER']),
        NumberRange(minimum=min_value, maximum=max_value, messages=answer_errors),
        DecimalPlaces(max_decimals=max_decimals, messages=answer_errors),
    ]

    if max_decimals > 0:
        return CustomDecimalField(
            label=label,
            validators=validate_with,
            description=guidance,
        )
    else:
        return CustomIntegerField(
            label=label,
            validators=validate_with,
            description=guidance,
        )


def get_schema_defined_limit(answer_id, definition, answer_store):
    value = None
    if definition:
        if 'value' in definition:
            value = definition['value']
        else:
            source_answer_id = definition.get('answer_id')
            answer_list = answer_store.filter(answer_id=source_answer_id)
            value = answer_list[0].get('value')
            if not isinstance(value, int) and not isinstance(value, Decimal):
                raise Exception('answer: {} value: {} for answer id: {} is not a valid number'
                                .format(answer_list[0].get('answer_id'), value, answer_id))

    return value
