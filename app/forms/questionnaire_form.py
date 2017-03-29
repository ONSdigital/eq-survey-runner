import logging

from wtforms import validators

from flask_wtf import FlaskForm

from app.forms.fields import get_field
from app.helpers.schema_helper import SchemaHelper
from app.validation.validators import DateRangeCheck

from werkzeug.datastructures import MultiDict

logger = logging.getLogger(__name__)


class QuestionnaireForm(FlaskForm):

    def __init__(self, block_json, formdata=None, **kwargs):
        self.block_json = block_json
        self.question_errors = {}
        self.options_with_children = {}

        if formdata:
            super().__init__(formdata=formdata, **kwargs)
        else:
            super().__init__(**kwargs)

    def validate(self):
        """
        Validate this form as usual and check for any form-level date-range validation errors
        :return:
        """
        valid_form = True
        valid_fields = FlaskForm.validate(self)

        for question_id, period_from_id, period_to_id in self.date_ranges:
            if period_from_id not in self.errors and period_to_id not in self.errors:
                period_from = getattr(self, period_from_id)
                period_to = getattr(self, period_to_id)
                validator = DateRangeCheck()

                # Check every field on each form has populated data
                populated = all([f.data for f in period_from] + [f.data for f in period_to])

                if populated:
                    try:
                        validator(self, period_from, period_to)
                    except validators.ValidationError as e:
                        self.question_errors[question_id] = str(e)
                        valid_form = False

        return valid_fields and valid_form

    def map_errors(self):
        ordered_errors = []

        question_json_list = SchemaHelper.get_questions_for_block(self.block_json)

        for question_json in question_json_list:
            if question_json['id'] in self.question_errors:
                ordered_errors += [(question_json['id'], self.question_errors[question_json['id']])]

            for answer_json in question_json['answers']:
                if answer_json['id'] in self.errors and 'parent_answer_id' not in answer_json:
                    ordered_errors += map_subfield_errors(self.errors, answer_json['id'])
                if 'options' in answer_json and 'parent_answer_id' not in answer_json:
                    ordered_errors += map_child_option_errors(self.errors, answer_json)

        return ordered_errors

    def answer_errors(self, input_id):
        return [error[1] for error in self.map_errors() if input_id == error[0]]

    def get_data(self, answer_id):
        attr = getattr(self, answer_id)
        return attr.raw_data[0] if attr.raw_data else ''

    def option_has_other(self, answer_id, option_index):
        if not self.options_with_children:
            self.options_with_children = SchemaHelper.get_parent_options_for_block(self.block_json)

        if answer_id in self.options_with_children and self.options_with_children[answer_id]['index'] == option_index:
            return True
        return False

    def get_other_answer(self, answer_id, option_index):
        if not self.options_with_children:
            self.options_with_children = SchemaHelper.get_parent_options_for_block(self.block_json)

        if answer_id in self.options_with_children and self.options_with_children[answer_id]['index'] == option_index:
            return getattr(self, self.options_with_children[answer_id]['child_answer_id'])
        return None


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
    answer_fields = {}

    class DynamicForm(QuestionnaireForm):
        date_ranges = []

    for question in SchemaHelper.get_questions_for_block(block_json):
        if question['type'] == 'DateRange':
            DynamicForm.date_ranges += [(question['id'], question['answers'][0]['id'], question['answers'][1]['id'])]
        answer_fields.update(get_answer_fields(question, data, error_messages))

    for answer_id, field in answer_fields.items():
        setattr(DynamicForm, answer_id, field)

    if data:
        form = DynamicForm(block_json, MultiDict(data))
    else:
        form = DynamicForm(block_json)

    return form
