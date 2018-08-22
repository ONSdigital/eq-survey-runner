from flask_wtf import FlaskForm
from wtforms import FieldList, SelectField, Label
from wtforms.compat import text_type
from werkzeug.datastructures import MultiDict

from app.forms.fields import build_choices, get_mandatory_validator
from app.data_model.answer_store import Answer
from app.jinja_filters import format_household_member_name


def build_relationship_choices(answer_store, group_instance):  # pylint: disable=too-many-locals
    """
    A function to build a list of tuples of as yet undefined person relationships

    :param answer_store: The answer store to use for current answers
    :param group_instance: The instance of the group being iterated over
    :return:
    """
    household_first_name_answers = answer_store.filter(answer_ids=['first-name'],
                                                       limit=True)
    household_last_name_answers = answer_store.filter(answer_ids=['last-name'],
                                                      limit=True)

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


def serialise_relationship_answers(answer_id, listfield_data, group_instance, group_instance_id):
    answers = []

    for index, listfield_value in enumerate(listfield_data):
        answer = Answer(
            answer_id=answer_id,
            answer_instance=index,
            group_instance=group_instance,
            group_instance_id=group_instance_id,
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


def generate_relationship_form(schema, block_json, relationship_choices, data, group_instance, group_instance_id):

    answer = schema.get_answers_for_block(block_json['id'])[0]

    class HouseHoldRelationshipForm(FlaskForm):
        question_errors = {}

        def map_errors(self):
            ordered_errors = []

            if self.errors:
                for answer_id, error_list in self.errors.items():
                    for errors in error_list:
                        for error in errors:
                            ordered_errors.append((answer_id, error))

            return ordered_errors

        def answer_errors(self, input_id):
            return [error[1] for error in self.map_errors() if input_id == error[0]]

        def serialise(self):
            """
            Returns a list of answers representing the form data
            :param location: The location to associate the form data with
            :return:
            """
            list_field = getattr(self, answer['id'])

            return serialise_relationship_answers(answer['id'], list_field.data, group_instance, group_instance_id)

    choices = [('', 'Select relationship')] + build_choices(answer['options'])

    labels = []

    for choice in relationship_choices:
        labels.append(answer.get('label') % dict(current_person=choice[0], other_person=choice[1]))

    field = FieldList(RelationshipSelectField(
        label=labels,
        choices=choices,
        validators=get_mandatory_validator(answer, schema.error_messages, 'MANDATORY_TEXTFIELD'),
    ), min_entries=len(relationship_choices))

    setattr(HouseHoldRelationshipForm, answer['id'], field)

    if data:
        form = HouseHoldRelationshipForm(MultiDict(data))
    else:
        form = HouseHoldRelationshipForm()

    return form


class RelationshipSelectField(SelectField):

    def __init__(self, label=None, validators=None, choices=None, **kwargs):
        super(RelationshipSelectField, self).__init__(label, validators, text_type, choices, **kwargs)

        index = int(self.id.rpartition('-')[-1])

        self.label = Label(self.id, self.label.text[index])
