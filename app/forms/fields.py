import logging

from wtforms import FormField, IntegerField, SelectField, SelectMultipleField, StringField, TextAreaField
from wtforms import validators
from wtforms.widgets import CheckboxInput, ListWidget, RadioInput, TextArea, TextInput

from app.forms.date_form import get_date_form, get_month_year_form
from app.validation.validators import IntegerCheck, PositiveIntegerCheck, NumberRange


logger = logging.getLogger(__name__)


def get_field(answer, label, error_messages):
    guidance = answer['guidance'] if 'guidance' in answer else ''

    field = {
        "Radio": get_select_field,
        "Checkbox": get_select_field,
        "Date": get_date_field,
        "MonthYearDate": get_date_field,
        "Currency": get_integer_field,
        "Integer": get_integer_field,
        "PositiveInteger": get_integer_field,
        "Percentage": get_integer_field,
        "TextArea": get_text_area_field,
        "TextField": get_string_field,
    }[answer['type']](answer, label, guidance, error_messages)

    if field is None:
        logger.info("Could not find field for answer type %s", answer['type'])

    return field


def build_choices(options):
    choices = []
    for option in options:
        choices.append((option['value'], option['label']))
    return choices


def get_validators(answer, error_messages):
    validate_with = [validators.optional()]

    if answer['mandatory'] is True:
        mandatory_message = error_messages['MANDATORY']

        if 'validation' in answer and 'messages' in answer['validation'] \
                and 'MANDATORY' in answer['validation']['messages']:
            mandatory_message = answer['validation']['messages']['MANDATORY']

        validate_with = [
            validators.InputRequired(
                message=mandatory_message,
            ),
        ]
    return validate_with


def get_string_field(answer, label, guidance, error_messages):
    validate_with = get_validators(answer, error_messages)

    return StringField(
        label=label,
        description=guidance,
        widget=TextArea(),
        validators=validate_with,
    )


def get_text_area_field(answer, label, guidance, error_messages):
    validate_with = get_validators(answer, error_messages)

    return TextAreaField(
        label=label,
        description=guidance,
        widget=TextArea(),
        validators=validate_with,
        filters=[lambda x: x if x else None],
    )


def get_date_field(answer, label, guidance, error_messages):

    if answer['type'] == 'MonthYearDate':
        return FormField(
            get_month_year_form(answer, error_messages),
            label=label,
            description=guidance,
        )
    else:
        return FormField(
            get_date_form(answer, error_messages=error_messages),
            label=label,
            description=guidance,
        )


def get_select_field(answer, label, guidance, error_messages):
    validate_with = get_validators(answer, error_messages)

    if answer['type'] == 'Checkbox':
        return SelectMultipleField(
            label=label,
            description=guidance,
            choices=build_choices(answer['options']),
            widget=ListWidget(),
            option_widget=CheckboxInput(),
            validators=validate_with,
        )
    else:
        return SelectField(
            label=label,
            description=guidance,
            choices=build_choices(answer['options']),
            widget=ListWidget(),
            option_widget=RadioInput(),
            validators=validate_with,
        )


def get_integer_field(answer, label, guidance, error_messages):
    answer_errors = error_messages.copy()

    if 'validation' in answer and 'messages' in answer['validation']:
        for error_key, error_message in answer['validation']['messages'].items():
            answer_errors[error_key] = error_message

    mandatory_or_optional = get_validators(answer, answer_errors)
    validate_with = mandatory_or_optional + [
        IntegerCheck(messages=answer_errors),
        NumberRange(max=9999999999, messages=answer_errors),
    ]

    if answer['type'] == 'Currency' or answer['type'] == 'PositiveInteger':
        validate_with += [PositiveIntegerCheck(messages=answer_errors)]
    elif answer['type'] == 'Percentage':
        validate_with = mandatory_or_optional + [
            IntegerCheck(messages=answer_errors),
            NumberRange(min=0, max=100, messages=answer_errors),
        ]

    return IntegerField(
        label=label,
        description=guidance,
        widget=TextInput(),
        validators=validate_with,
    )
