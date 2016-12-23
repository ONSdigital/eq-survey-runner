from flask_wtf import FlaskForm
from wtforms import FieldList, SelectField
from wtforms.widgets import ListWidget, RadioInput

from app.forms.questionnaire_form import Struct
from app.forms.fields import build_choices, get_validators
from app.helpers.schema_helper import SchemaHelper
from app.jinja_filters import format_household_member_name


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


def generate_relationship_form(block_json, number_of_entries, data, error_messages):
    class HouseHoldRelationshipForm(FlaskForm):
        def map_errors(self):
            ordered_errors = []

            if len(self.errors) > 0:
                for answer_id, error_list in self.errors.items():
                    for errors in error_list:
                        for error in errors:
                            ordered_errors.append((answer_id, error))

            return ordered_errors

    answer = SchemaHelper.get_first_answer_for_block(block_json)
    guidance = answer['guidance'] if 'guidance' in answer else ''
    label = answer['label'] if 'label' in answer else ''

    field = FieldList(SelectField(
        label=label,
        description=guidance,
        choices=build_choices(answer['options']),
        widget=ListWidget(),
        option_widget=RadioInput(),
        validators=get_validators(answer, error_messages),
    ), min_entries=number_of_entries)

    setattr(HouseHoldRelationshipForm, answer['id'], field)

    if data:
        data_class = Struct(**data)
        form = HouseHoldRelationshipForm(meta={'csrf': False}, obj=data_class)
    else:
        form = HouseHoldRelationshipForm(meta={'csrf': False})

    return form
