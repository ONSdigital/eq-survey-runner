from flask_wtf import FlaskForm
from wtforms import FieldList, SelectField

from app import settings
from app.forms.fields import build_choices, get_mandatory_validator
from app.data_model.answer_store import Answer
from app.helpers.schema_helper import SchemaHelper
from app.jinja_filters import format_household_member_name

from werkzeug.datastructures import MultiDict


def build_relationship_choices(answer_store, group_instance):
    """
    A function to build a list of tuples of as yet undefined person relationships

    :param answer_store: The answer store to use for current answers
    :param group_instance: The instance of the group being iterated over
    :return:
    """
    household_first_name_answers = answer_store.filter(block_id='household-composition', answer_id='first-name', limit=settings.EQ_MAX_NUM_REPEATS)
    household_last_name_answers = answer_store.filter(block_id='household-composition', answer_id='last-name', limit=settings.EQ_MAX_NUM_REPEATS)

    first_names = []
    last_names = []

    for answer in household_first_name_answers:
        first_names.append(answer['value'])

    for answer in household_last_name_answers:
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


def serialise_relationship_answers(location, answer_id, listfield_data):
    answers = []
    for index, listfield_value in enumerate(listfield_data):
        answer = Answer(
            location=location,
            answer_id=answer_id,
            answer_instance=index,
            value=listfield_value,
        )
        answers.append(answer)
    return answers


def deserialise_relationship_answers(answers):
    relationships = {}

    for answer in answers:
        relationship_id = '{answer_id}-{index}'.format(
            answer_id=answer['answer_id'],
            index=answer['answer_instance'],
        )
        relationships[relationship_id] = answer['value']

    return relationships


def generate_relationship_form(block_json, number_of_entries, data, error_messages):

    answer = SchemaHelper.get_first_answer_for_block(block_json)

    class HouseHoldRelationshipForm(FlaskForm):
        question_errors = {}

        def map_errors(self):
            ordered_errors = []

            if len(self.errors) > 0:
                for answer_id, error_list in self.errors.items():
                    for errors in error_list:
                        for error in errors:
                            ordered_errors.append((answer_id, error))

            return ordered_errors

        def answer_errors(self, input_id):
            return [error[1] for error in self.map_errors() if input_id == error[0]]

        def serialise(self, location):
            """
            Returns a list of answers representing the form data
            :param location: The location to associate the form data with
            :return:
            """
            list_field = getattr(self, answer['id'])

            return serialise_relationship_answers(location, answer['id'], list_field.data)

    choices = [('', 'Select relationship')] + build_choices(answer['options'])

    field = FieldList(SelectField(
        label=answer.get('guidance'),
        description=answer.get('label'),
        choices=choices,
        default='',
        validators=get_mandatory_validator(answer, error_messages),
    ), min_entries=number_of_entries)

    setattr(HouseHoldRelationshipForm, answer['id'], field)

    if data:
        form = HouseHoldRelationshipForm(MultiDict(data))
    else:
        form = HouseHoldRelationshipForm()

    return form
