import logging

from flask_wtf import FlaskForm

from app.forms.date_form import get_date_data, get_date_range_fields
from app.forms.fields import get_field
from app.helpers.schema_helper import SchemaHelper

from werkzeug.datastructures import MultiDict

logger = logging.getLogger(__name__)


def get_date_range_field(question, data, error_messages):
    to_field_id = question['answers'][1]['id']
    to_field_data = get_date_data(data, to_field_id)

    from_field, to_field = get_date_range_fields(question, to_field_data, error_messages)

    return {
        question['answers'][0]['id']: from_field,
        question['answers'][1]['id']: to_field,
    }


def get_answer_fields(question, data, error_messages):
    answer_fields = {}
    for answer in question['answers']:
        if 'parent_answer_id' in answer and answer['parent_answer_id'] in data and \
                data[answer['parent_answer_id']] == 'Other':
            answer['mandatory'] = \
                next(a['mandatory'] for a in question['answers'] if a['id'] == answer['parent_answer_id'])

        name = answer.get('label') or question.get('title')
        answer_fields[answer['id']] = get_field(answer, name, error_messages)
    return answer_fields


def map_subfield_errors(errors, answer_id):
    subfield_errors = []

    if isinstance(errors[answer_id], dict):
        for error_list in errors[answer_id].values():
            for error in error_list:
                subfield_errors.append((answer_id, error))
    else:
        for error in errors[answer_id]:
            subfield_errors.append((answer_id, error))

    return subfield_errors


def map_child_option_errors(errors, answer_json):
    child_errors = []
    options_with_children = [o for o in answer_json['options'] if
                             'child_answer_id' in o and o['child_answer_id'] in errors]

    for option_with_child in options_with_children:
        for error in errors[option_with_child['child_answer_id']]:
            child_errors.append((answer_json['id'], error))

    return child_errors


def generate_form(block_json, data, error_messages):

    class QuestionnaireForm(FlaskForm):
        def map_errors(self):
            ordered_errors = []

            answer_json_list = SchemaHelper.get_answers_for_block(block_json)

            for answer_json in answer_json_list:
                if answer_json['id'] in self.errors and 'parent_answer_id' not in answer_json:
                    ordered_errors += map_subfield_errors(self.errors, answer_json['id'])
                if 'options' in answer_json and 'parent_answer_id' not in answer_json:
                    ordered_errors += map_child_option_errors(self.errors, answer_json)

            return ordered_errors

        def answer_errors(self, input_id):
            return [error[1] for error in self.map_errors() if input_id == error[0]]

    answer_fields = {}

    for question in SchemaHelper.get_questions_for_block(block_json):
        if question['type'] == 'DateRange':
            answer_fields.update(get_date_range_field(question, data, error_messages))
        else:
            answer_fields.update(get_answer_fields(question, data, error_messages))

    for answer_id, field in answer_fields.items():
        setattr(QuestionnaireForm, answer_id, field)

    if data:
        form = QuestionnaireForm(MultiDict(data), meta={'csrf': False})
    else:
        form = QuestionnaireForm(meta={'csrf': False})

    return form
