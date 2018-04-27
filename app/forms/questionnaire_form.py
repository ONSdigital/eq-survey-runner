import logging
from datetime import datetime, timedelta

from decimal import Decimal

import itertools

from dateutil.relativedelta import relativedelta
from wtforms import validators
from flask_wtf import FlaskForm
from werkzeug.datastructures import MultiDict

from app.forms.fields import get_field
from app.forms.date_form import get_dates_for_single_date_period_validation
from app.validation.validators import DateRangeCheck, SumCheck

logger = logging.getLogger(__name__)


class QuestionnaireForm(FlaskForm):

    def __init__(self, schema, block_json, answer_store, metadata, formdata=None, **kwargs):
        self.schema = schema
        self.block_json = block_json
        self.answer_store = answer_store
        self.metadata = metadata
        self.question_errors = {}
        self.options_with_children = {}

        if formdata:
            super().__init__(formdata=formdata, **kwargs)
        else:
            super().__init__(**kwargs)

    def validate(self):
        """
        Validate this form as usual and check for any form-level date-range/calculated validation errors
        :return:
        """
        valid_fields = FlaskForm.validate(self)
        valid_date_range_form = True
        valid_calculated_form = True

        for question in self.schema.get_questions_for_block(self.block_json):
            if question['type'] == 'DateRange':
                valid_date_range = self.validate_date_range_question(question)
                if valid_date_range_form:
                    valid_date_range_form = valid_date_range
            elif question['type'] == 'Calculated':
                valid_calculated = self.validate_calculated_question(question)
                if valid_calculated_form:
                    valid_calculated_form = valid_calculated

        return valid_calculated_form and valid_date_range_form and valid_fields

    def validate_date_range_question(self, question):
        date_from = question['answers'][0]
        date_to = question['answers'][1]
        if self._has_min_and_max_single_dates(date_from, date_to):
            # Work out the largest possible range, for date range question
            period_range = self._get_period_range_for_single_date(date_from, date_to)
            if 'period_limits' in question:
                self.validate_date_range_with_period_limits_and_single_date_limits(question['id'],
                                                                                   question['period_limits'],
                                                                                   period_range)
            else:
                # Check every field on each form has populated data
                if self.is_date_form_populated(getattr(self, date_from['id']), getattr(self, date_to['id'])):
                    self.validate_date_range_with_single_date_limits(question['id'], period_range)
        period_from_id = date_from['id']
        period_to_id = date_to['id']
        messages = None
        if 'validation' in question:
            messages = question['validation'].get('messages')

        if not (
                self.answers_all_valid([period_from_id, period_to_id]) and
                self._validate_date_range_question(question['id'], period_from_id, period_to_id, messages,
                                                   question.get('period_limits'))):
            return False

        return True

    def validate_calculated_question(self, question):
        for calculation in question['calculations']:
            target_total, currency = self._get_target_total_and_currency(calculation, question)
            if (self.answers_all_valid(calculation['answers_to_calculate']) and
                    self._validate_calculated_question(calculation, question, target_total, currency)):
                # Remove any previous question errors if it passes this OR before returning True
                if question['id'] in self.question_errors:
                    self.question_errors.pop(question['id'])
                return True

        return False

    def _get_target_total_and_currency(self, calculation, question):
        if 'value' in calculation:
            return calculation['value'], question.get('currency')

        target_answer = self.schema.get_answer(calculation['answer_id'])
        return self.answer_store.filter(answer_ids=[target_answer['id']]).values()[0], target_answer.get('currency')

    def validate_date_range_with_period_limits_and_single_date_limits(self, question_id, period_limits, period_range):
        # Get period_limits from question
        period_min = self._get_period_limits(period_limits)[0]
        min_offset = self._get_offset_value(period_min)

        # Exception to be raised if range available is smaller than minimum range allowed
        if period_min and period_range < min_offset:
            exception = 'The schema has invalid period_limits for {}'.format(question_id)
            raise Exception(exception)

    @staticmethod
    def validate_date_range_with_single_date_limits(question_id, period_range):
        # Exception to be raised if range from answers are smaller than
        # minimum or larger than maximum period_limits
        exception = 'The schema has invalid date answer limits for {}'.format(question_id)

        if period_range < timedelta(0):
            raise Exception(exception)

    def _validate_date_range_question(self, question_id, period_from_id, period_to_id, messages, period_limits):
        period_from = getattr(self, period_from_id)
        period_to = getattr(self, period_to_id)
        period_min, period_max = self._get_period_limits(period_limits)
        validator = DateRangeCheck(messages=messages, period_min=period_min, period_max=period_max)

        # Check every field on each form has populated data
        if self.is_date_form_populated(period_from, period_to):
            try:
                validator(self, period_from, period_to)
            except validators.ValidationError as e:
                self.question_errors[question_id] = str(e)
                return False

        return True

    def _validate_calculated_question(self, calculation, question, target_total, currency):
        messages = None
        if 'validation' in question:
            messages = question['validation'].get('messages')

        validator = SumCheck(messages=messages, currency=currency)

        calculation_type = self._get_calculation_type(calculation['calculation_type'])

        formatted_values = self._get_formatted_calculation_values(calculation['answers_to_calculate'])

        calculation_total = self._get_calculation_total(calculation_type, formatted_values)

        # Validate grouped answers meet calculation_type criteria
        try:
            validator(self, calculation['conditions'], calculation_total, target_total)
        except validators.ValidationError as e:
            self.question_errors[question['id']] = str(e)
            return False

        return True

    def _get_period_range_for_single_date(self, date_from, date_to):
        from_min_period_date, from_max_period_date = get_dates_for_single_date_period_validation(date_from,
                                                                                                 self.answer_store,
                                                                                                 self.metadata)
        to_min_period_date, to_max_period_date = get_dates_for_single_date_period_validation(date_to,
                                                                                             self.answer_store,
                                                                                             self.metadata)

        min_period_date = from_min_period_date or from_max_period_date
        max_period_date = to_max_period_date or to_min_period_date

        # Work out the largest possible range, for date range question
        period_range = max_period_date - min_period_date

        return period_range

    @staticmethod
    def is_date_form_populated(date_from, date_to):
        return all(field.data for field in itertools.chain(date_from, date_to))

    @staticmethod
    def _has_min_and_max_single_dates(date_from, date_to):
        return ('minimum' in date_from or 'maximum' in date_from) and ('minimum' in date_to or 'maximum' in date_to)

    @staticmethod
    def _get_offset_value(period_object):
        now = datetime.now()
        delta = relativedelta(years=period_object.get('years', 0),
                              months=period_object.get('months', 0),
                              days=period_object.get('days', 0))

        return now + delta - now

    @staticmethod
    def _get_period_limits(limits):
        minimum, maximum = None, None
        if limits:
            if 'minimum' in limits:
                minimum = limits['minimum']
            if 'maximum' in limits:
                maximum = limits['maximum']
        return minimum, maximum

    @staticmethod
    def _get_calculation_type(calculation_type):
        if calculation_type == 'sum':
            return sum
        else:
            error = 'Invalid calculation_type: {}'.format(calculation_type)
            raise Exception(error)

    def _get_formatted_calculation_values(self, answers_list):
        return[self.get_data(answer_id).replace(' ', '').replace(',', '') for answer_id in answers_list]

    @staticmethod
    def _get_calculation_total(calculation_type, values):
        return calculation_type(Decimal(value or 0) for value in values)

    def answers_all_valid(self, answer_id_list):
        return not set(answer_id_list) & set(self.errors)

    def map_errors(self):
        ordered_errors = []

        question_json_list = self.schema.get_questions_for_block(self.block_json)

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
            self.options_with_children = self.schema.get_parent_options_for_block(self.block_json['id'])

        if answer_id in self.options_with_children and self.options_with_children[answer_id]['index'] == option_index:
            return True
        return False

    def get_other_answer(self, answer_id, option_index):
        if not self.options_with_children:
            self.options_with_children = self.schema.get_parent_options_for_block(self.block_json['id'])

        if answer_id in self.options_with_children and self.options_with_children[answer_id]['index'] == option_index:
            return getattr(self, self.options_with_children[answer_id]['child_answer_id'])
        return None


def get_answer_fields(question, data, error_messages, answer_store, metadata):
    answer_fields = {}
    for answer in question['answers']:
        if 'parent_answer_id' in answer and answer['parent_answer_id'] in data and \
                data[answer['parent_answer_id']] == 'Other':
            answer['mandatory'] = \
                next(a['mandatory'] for a in question['answers'] if a['id'] == answer['parent_answer_id'])

        name = answer.get('label') or question.get('title')
        answer_fields[answer['id']] = get_field(answer, name, error_messages, answer_store, metadata)
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


def generate_form(schema, block_json, data, answer_store, metadata):
    answer_fields = {}

    class DynamicForm(QuestionnaireForm):
        for question in schema.get_questions_for_block(block_json):
            answer_fields.update(get_answer_fields(question, data, schema.error_messages, answer_store, metadata))

    for answer_id, field in answer_fields.items():
        setattr(DynamicForm, answer_id, field)

    if data:
        form = DynamicForm(schema, block_json, answer_store, metadata, MultiDict(data))
    else:
        form = DynamicForm(schema, block_json, answer_store, metadata)

    return form
