import calendar
import logging

from datetime import datetime

from app.helpers.schema_helper import SchemaHelper
from app.jinja_filters import format_household_member_name
from app.validation.error_messages import error_messages
from app.validation.validators import positive_integer_type_check, date_range_check

from flask_wtf import FlaskForm

from wtforms import FieldList, Form, FormField, IntegerField, SelectField, SelectMultipleField, StringField, TextAreaField
from wtforms import validators
from wtforms.widgets import CheckboxInput, ListWidget, RadioInput, TextArea, TextInput


logger = logging.getLogger(__name__)


def build_relationship_choices(answer_store, group_instance):
    household_answers = answer_store.filter(answer_id='household')

    first_names = [answer['first_name'] for answer in household_answers[0]['value']]
    last_names = [answer['last_name'] for answer in household_answers[0]['value']]

    household_members = []

    for first_name, last_name in zip(first_names, last_names):
        household_members.append({
            'first-name': first_name,
            'last-name': last_name,
        })

    remaining_people = household_members[group_instance + 1:] if group_instance < len(household_members) else []

    current_person_name = format_household_member_name([
        household_members[group_instance]['first-name'],
        household_members[group_instance]['last-name'],
    ])

    choices = []

    for index, remaining_person in enumerate(remaining_people):
        other_person_name = format_household_member_name([
            remaining_person['first-name'],
            remaining_person['last-name'],
        ])
        choices.append((current_person_name, other_person_name))

    return choices


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


def generate_relationship_form(block_json, number_of_entries, data):
    class HouseHoldRelationshipForm(FlaskForm):
        pass

    answer = SchemaHelper.get_first_answer_for_block(block_json)
    guidance = answer['guidance'] if 'guidance' in answer else ''
    label = answer['label'] if 'label' in answer else ''

    field = FieldList(SelectField(
        label=label,
        description=guidance,
        choices=build_choices(answer['options']),
        widget=ListWidget(),
        option_widget=RadioInput(),
    ), min_entries=number_of_entries)

    setattr(HouseHoldRelationshipForm, answer['id'], field)

    if data:
        data_class = Struct(**data)
        form = HouseHoldRelationshipForm(csrf_enabled=False, obj=data_class)
    else:
        form = HouseHoldRelationshipForm(csrf_enabled=False)

    return form


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
