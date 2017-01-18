import calendar
import logging

from app.data_model.answer_store import Answer
from app.helpers.schema_helper import SchemaHelper
from app.jinja_filters import format_household_member_name
from app.validation.error_messages import error_messages
from app.validation.validators import DateRangeCheck, DateCheck, MonthYearCheck, positive_integer_type_check

from flask_wtf import FlaskForm

from wtforms import FieldList, Form, FormField, IntegerField, SelectField, SelectMultipleField, StringField, TextAreaField
from wtforms import validators
from wtforms.widgets import CheckboxInput, ListWidget, RadioInput, TextArea, TextInput


logger = logging.getLogger(__name__)


def build_choices(options):
    choices = []
    for option in options:
        choices.append((option['value'], option['label']))
    return choices


def build_relationship_choices(answer_store, group_instance):
    """
    A function to build a list of tuples of as yet undefined person relationships

    :param answer_store: The answer store to use for current answers
    :param group_instance: The instance of the group being iterated over
    :return:
    """
    household_answers = answer_store.filter(block_id='household-composition')

    first_names = []
    last_names = []

    for answer in household_answers:
        if answer['answer_id'] == 'first-name':
            first_names.append(answer['value'])
        if answer['answer_id'] == 'last-name':
            last_names.append(answer['value'])

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

    for remaining_person in remaining_people:
        other_person_name = format_household_member_name([
            remaining_person['first-name'],
            remaining_person['last-name'],
        ])
        choices.append((current_person_name, other_person_name))

    return choices


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


def get_date_form(answer=None, to_field_data=None, validate_range=False):
    """
    Returns a date form metaclass with appropriate validators. Used in both date and
    date range form creation.

    :param answer: The answer on which to base this form
    :param to_field_data: The data coming from the
    :param validate_range: Whether the dateform should add a daterange validator
    :return:
    """
    class DateForm(Form):

        MONTH_CHOICES = [('', 'Select month')] + [(str(x), calendar.month_name[x]) for x in range(1, 13)]

        month = SelectField(choices=MONTH_CHOICES, default='')
        year = StringField()

    validate_with = []

    if answer['mandatory'] is False:
        validate_with += [validators.optional()]

    if 'validation' in answer and 'messages' in answer['validation'] \
        and 'INVALID_DATE' in answer['validation']['messages']:
        error_message = answer['validation']['messages']['INVALID_DATE']
        validate_with += [DateCheck(error_message)]

    if validate_range and to_field_data:
        validate_with += [DateRangeCheck(to_field_data=to_field_data)]

    DateForm.day = StringField(validators=validate_with)

    return DateForm


def get_month_year_form(answer):

    class MonthYearDateForm(Form):
        year = StringField()

    month_choices = [('', 'Select month')] + [(str(x), calendar.month_name[x]) for x in range(1, 13)]

    validate_with = [MonthYearCheck()]

    if 'validation' in answer and 'messages' in answer['validation'] \
        and 'INVALID_DATE' in answer['validation']['messages']:
        error_message = answer['validation']['messages']['INVALID_DATE']
        validate_with = [MonthYearCheck(error_message)]

    if answer['mandatory'] is False:
        validate_with += [validators.optional()]

    MonthYearDateForm.month = SelectField(choices=month_choices, default='', validators=validate_with)

    return MonthYearDateForm


def get_name_form():
    class NameForm(Form):
        pass

    first_name = StringField(validators=[
        validators.InputRequired(
            message=error_messages['MANDATORY'],
        ),
    ])

    middle_names = StringField(validators=[validators.Optional()])
    last_name = StringField(validators=[validators.Optional()])

    # Have to be set this way given hyphenated names
    # are considered invalid in python
    setattr(NameForm, 'first-name', first_name)
    setattr(NameForm, 'middle-names', middle_names)
    setattr(NameForm, 'last-name', last_name)

    return NameForm


def get_date_range_fields(question_json, to_field_data):
    answer_from = question_json['answers'][0]
    answer_to = question_json['answers'][1]

    field_from = FormField(
        get_date_form(answer=answer_from, to_field_data=to_field_data, validate_range=True),
        label=answer_from['label'] if 'label' in answer_from else '',
        description=answer_from['guidance'] if 'guidance' in answer_from else '',
    )
    field_to = FormField(
        get_date_form(answer=answer_to),
        label=answer_to['label'] if 'label' in answer_to else '',
        description=answer_to['guidance'] if 'guidance' in answer_to else '',
    )

    return field_from, field_to


def deserialise_composition_answers(answers):
    household = []
    answer_instance = 0

    while any([a for a in answers if a['answer_instance'] == answer_instance]):
        instance_answers = [a for a in answers if a['answer_instance'] == answer_instance]
        person = {}
        for instance_answer in instance_answers:
            person[instance_answer['answer_id']] = instance_answer['value']
        household.append(person)

        answer_instance += 1
    return household


class HouseHoldCompositionForm(FlaskForm):
    household = FieldList(FormField(get_name_form()), min_entries=1)

    def remove_person(self, index_to_remove):
        popped = []

        while index_to_remove != len(self.household.data):
            popped.append(self.household.pop_entry())

        popped.reverse()

        for field in popped[1:]:
            self.household.append_entry(field.data)

    def serialise(self, location):
        """
        Returns a list of answers representing the form data
        :param location: The location to associate the form data with
        :return:
        """
        answers = []
        for index, person_data in enumerate(self.household.data):
            for answer_id, answer_value in person_data.items():
                answer = Answer(
                    location=location,
                    answer_id=answer_id,
                    answer_instance=index,
                    value=person_data[answer_id],
                )
                answers.append(answer)
        return answers


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


def get_date_data(form_data, answer_id):
    """
    Extract date from a form and return as a dict that wtforms would use

    :param form_data: The form data to search through
    :param answer_id: The answer_id to search for
    :return:
    """
    day_id = answer_id + '-day'
    month_id = answer_id + '-month'
    year_id = answer_id + '-year'

    if all(x in form_data for x in [day_id, month_id, year_id]):
        return {
            'day': form_data[day_id],
            'month': form_data[month_id],
            'year': form_data[year_id],
        }
    return None


def generate_form(block_json, data):
    class QuestionnaireForm(FlaskForm):
        pass

    for section in block_json['sections']:
        for question in section['questions']:
            if question['type'] == 'DateRange':
                to_field_id = question['answers'][1]['id']
                to_field_data = get_date_data(data, to_field_id)

                from_field, to_field = get_date_range_fields(question, to_field_data)

                setattr(QuestionnaireForm, question['answers'][0]['id'], from_field)
                setattr(QuestionnaireForm, question['answers'][1]['id'], to_field)
            else:
                for answer in question['answers']:
                    if 'parent_answer_id' in answer and answer['parent_answer_id'] in data and \
                            data[answer['parent_answer_id']] == 'Other':
                        answer['mandatory'] = \
                            next(a['mandatory'] for a in question['answers'] if a['id'] == answer['parent_answer_id'])

                    name = answer['label'] if 'label' in answer else question['title']
                    setattr(QuestionnaireForm, answer['id'], get_field(answer, name))
    if data:
        data_class = Struct(**data)
        form = QuestionnaireForm(csrf_enabled=False, obj=data_class)
    else:
        form = QuestionnaireForm(csrf_enabled=False)

    return form


def get_field(answer, label):
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
    }[answer['type']](answer, label, guidance)

    if field is None:
        logger.info("Could not find field for answer type %s", answer['type'])

    return field


def get_validators(answer):
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


def get_string_field(answer, label, guidance):
    validate_with = get_validators(answer)

    return StringField(
        label=label,
        description=guidance,
        widget=TextArea(),
        validators=validate_with,
    )


def get_text_area_field(answer, label, guidance):
    validate_with = get_validators(answer)

    return TextAreaField(
        label=label,
        description=guidance,
        widget=TextArea(),
        validators=validate_with,
        filters=[lambda x: x if x else None],
    )


def get_date_field(answer, label, guidance):

    if answer['type'] == 'MonthYearDate':
        return FormField(
            get_month_year_form(answer),
            label=label,
            description=guidance,
        )
    else:
        return FormField(
            get_date_form(answer),
            label=label,
            description=guidance,
        )


def get_select_field(answer, label, guidance):
    validate_with = get_validators(answer)

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


def get_integer_field(answer, label, guidance):
    validate_with = get_validators(answer)

    if answer['type'] == 'Currency':
        validate_with += [
            positive_integer_type_check,
        ]

    if answer['type'] == 'Percentage':
        validate_with += [
            validators.NumberRange(min=0, max=100),
        ]

    if answer['type'] == 'PositiveInteger':
        validate_with += [
            validators.NumberRange(min=0),
        ]

    return IntegerField(
        label=label,
        description=guidance,
        widget=TextInput(),
        validators=validate_with,
    )
