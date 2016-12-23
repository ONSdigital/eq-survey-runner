import calendar
import logging

from datetime import datetime

from app.validation.error_messages import error_messages

from flask_wtf import FlaskForm

from wtforms import FieldList, Form, FormField, IntegerField, SelectField, SelectMultipleField, StringField, TextAreaField
from wtforms import validators
from wtforms.widgets import CheckboxInput, ListWidget, RadioInput, TextArea, TextInput


logger = logging.getLogger(__name__)


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


class DateForm(Form):

    MONTH_CHOICES = [(str(x), calendar.month_name[x]) for x in range(1, 13)]

    day = StringField()
    month = SelectField(choices=MONTH_CHOICES)
    year = StringField()

    def to_date(self):
        datestr = "{:02d}/{:02d}/{}".format(int(self.day.data or 0), int(self.month.data or 0), self.year.data or '')

        return datetime.strptime(datestr, "%d/%m/%Y")

    def validate_day(self, field=None):
        try:
            self.to_date()
        except ValueError:
            raise validators.ValidationError(error_messages['INVALID_DATE'])
        return True


class NameForm(Form):
    first_name = StringField(validators=[
        validators.InputRequired(
            message=error_messages['MANDATORY'],
        ),
    ])

    middle_names = StringField(validators=[validators.Optional()])
    last_name = StringField(validators=[validators.Optional()])


class HouseHoldCompositionForm(FlaskForm):
    household = FieldList(FormField(NameForm), min_entries=1)

    def remove_person(self, index_to_remove):
        popped = []

        while index_to_remove != len(self.household.data):
            popped.append(self.household.pop_entry())

        popped.reverse()

        for field in popped[1:]:
            self.household.append_entry(field.data)


def generate_form(block_json, data):
    class QuestionnaireForm(FlaskForm):
        pass

    for section in block_json['sections']:
        for question in section['questions']:
            for answer in question['answers']:
                name = answer['label'] if 'label' in answer else question['title']
                setattr(QuestionnaireForm, answer['id'], get_field(answer, name))

    if data:
        data_class = Struct(**data)
        form = QuestionnaireForm(csrf_enabled=False, obj=data_class)
    else:
        form = QuestionnaireForm(csrf_enabled=False)

    return form


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


def get_field(answer, label):
    field = None
    guidance = answer['guidance'] if 'guidance' in answer else ''

    if answer['type'] == 'Radio':
        field = SelectField(
            label=label,
            description=guidance,
            choices=build_choices(answer['options']),
            widget=ListWidget(),
            option_widget=RadioInput(),
        )
    if answer['type'] == 'Checkbox':
        field = SelectMultipleField(
            label=label,
            description=guidance,
            choices=build_choices(answer['options']),
            widget=ListWidget(),
            option_widget=CheckboxInput(),
        )
    if answer['type'] == 'Date':
        field = FormField(
            DateForm,
            label=label,
            description=guidance,
        )
    if answer['type'] == 'Currency':
        if answer['mandatory'] is True:
            field = IntegerField(
                label=label,
                description=guidance,
                widget=TextInput(),
                validators=[
                    validators.InputRequired(
                        message=answer['validation']['messages']['MANDATORY'] or error_messages['MANDATORY']
                    ),
                    positive_integer_type_check,
                ],
            )
        else:
            label = '<span class="label__inner">'+label+'</span>'
            field = IntegerField(
                label=label,
                description=guidance,
                widget=TextInput(),
                validators=[
                    validators.Optional(),
                ],
            )
    if answer['type'] == 'PositiveInteger' or answer['type'] == 'Integer':
        if answer['mandatory'] is True:
            field = IntegerField(
                label=label,
                description=guidance,
                widget=TextInput(),
                validators=[
                    validators.InputRequired(
                        message=answer['validation']['messages']['MANDATORY'] or error_messages['MANDATORY']
                    ),
                ],
            )
        else:
            label = '<span class="label__inner">'+label+'</span>'
            field = IntegerField(
                label=label,
                description=guidance,
                widget=TextInput(),
                validators=[
                    validators.Optional(),
                ],
            )
    if answer['type'] == 'TextArea':
        field = TextAreaField(
            label=label,
            description=guidance,
            widget=TextArea(),
            validators=[
                validators.Optional(),
            ],
            filters=[lambda x: x if x else None],
        )
    if answer['type'] == 'TextField':
        field = StringField(
            label=label,
            description=guidance,
            widget=TextArea(),
            validators=[
                validators.Optional(),
            ],
        )

    if field is None:
        logger.info("Could not find field for answer type %s", answer['type'])

    return field


def build_choices(options):
    choices = []
    for option in options:
        choices.append((option['label'], option['value']))
    return choices
