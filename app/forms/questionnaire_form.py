import logging

from flask_wtf import FlaskForm

from app.forms.date_form import get_date_data, get_date_range_fields
from app.forms.fields import get_field
from app.helpers.schema_helper import SchemaHelper

from werkzeug.datastructures import MultiDict

logger = logging.getLogger(__name__)


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


def get_date_range_answer_field(question, data, error_messages):
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

        name = answer['label'] if 'label' in answer else question['title']
        answer_fields[answer['id']] = get_field(answer, name, error_messages)
    return answer_fields


def map_subfield_errors(errors, answer_id):
    subfield_errors = []

    if isinstance(errors[answer_id], dict):
        for subfield, errors in errors[answer_id].items():
            for error in errors:
                subfield_errors.append((answer_id, error))
    else:
        for error in errors[answer_id]:
            subfield_errors.append((answer_id, error))

    return subfield_errors


def map_child_errors(errors, parent_answer_id, child_answer_id):
    child_errors = []
    for error in errors[child_answer_id]:
        child_errors.append((parent_answer_id, error))
    return child_errors


def generate_form(block_json, data, error_messages):

    class QuestionnaireForm(FlaskForm):
        def map_errors(self):
            ordered_errors = []

            answer_json_list = SchemaHelper.get_answers_for_block(block_json)

            for answer_json in answer_json_list:
                if answer_json['id'] in self.errors:
                    ordered_errors += map_subfield_errors(self.errors, answer_json['id'])
                if 'child_answer_id' in answer_json and answer_json['child_answer_id'] in self.errors:
                    ordered_errors += map_child_errors(self.errors, answer_json['id'], answer_json['child_answer_id'])
            return ordered_errors

    answer_fields = {}

    for question in SchemaHelper.get_questions_for_block(block_json):
        if question['type'] == 'DateRange':
            answer_fields.update(get_date_range_answer_field(question, data, error_messages))
        else:
            answer_fields.update(get_answer_fields(question, data, error_messages))

    for answer_id, field in answer_fields.items():
        setattr(QuestionnaireForm, answer_id, field)

    if data:
        form = QuestionnaireForm(MultiDict(data), meta={'csrf': False})
    else:
        form = QuestionnaireForm(meta={'csrf': False})

    return form
