from structlog import get_logger
from flask_wtf import FlaskForm
from wtforms import FieldList, Form, FormField

from app.data_model.answer_store import Answer
from app.forms.fields import get_string_field

from werkzeug.datastructures import MultiDict


logger = get_logger()


def get_name_form(schema, block_json):
    class NameForm(Form):
        pass

    for question in schema.get_questions_for_block(block_json):
        for answer in question['answers']:
            guidance = answer.get('guidance', '')
            label = answer.get('label') or question.get('title')

            field = get_string_field(answer, label, guidance, schema.error_messages)

            setattr(NameForm, answer['id'], field)

    return NameForm


def serialise_composition_answers(location, data):
    answers = []
    for index, person_data in enumerate(data):
        for answer_id in person_data.keys():
            answer = Answer(
                location=location,
                answer_id=answer_id,
                answer_instance=index,
                value=person_data[answer_id],
            )
            answers.append(answer)
    return answers


def deserialise_composition_answers(answers):
    household = {}

    for answer in answers:
        composition_id = 'household-{index}-{subfield}'.format(
            index=answer['answer_instance'],
            subfield=answer['answer_id'],
        )
        household[composition_id] = answer['value']

    return household


def map_field_errors(errors, index):
    ordered_errors = []
    for subfield, errorlist in errors.items():
        answer_id = 'household-{index}-{subfield}'.format(index=index, subfield=subfield)
        for error in errorlist:
            ordered_errors.append((answer_id, error))
    return ordered_errors


def generate_household_composition_form(schema, block_json, data):
    class HouseHoldCompositionForm(FlaskForm):
        question_errors = {}
        household = FieldList(FormField(get_name_form(schema, block_json)), min_entries=1)

        def map_errors(self):
            ordered_errors = []

            if 'household' in self.errors and self.errors['household']:
                for index, field in enumerate(self.household):
                    ordered_errors += map_field_errors(field.errors, index)
            return ordered_errors

        def answer_errors(self, input_id):
            return [error[1] for error in self.map_errors() if input_id == error[0]]

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
            return serialise_composition_answers(location, self.household.data)

    return HouseHoldCompositionForm(MultiDict(data))
