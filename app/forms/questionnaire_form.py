import itertools
import logging
from datetime import datetime, timedelta
from decimal import Decimal

from dateutil.relativedelta import relativedelta
from flask_wtf import FlaskForm
from werkzeug.datastructures import MultiDict
from wtforms import validators

from app.forms.date_form import get_dates_for_single_date_period_validation
from app.forms.fields import get_field
from app.templating.utils import get_question_title
from app.validation.validators import DateRangeCheck, SumCheck, MutuallyExclusiveCheck

logger = logging.getLogger(__name__)


class QuestionnaireForm(FlaskForm):

    def __init__(self, schema, block_json, answer_store, metadata, **kwargs):
        self.schema = schema
        self.block_json = block_json
        self.answer_store = answer_store
        self.metadata = metadata
        self.question_errors = {}
        self.options_with_detail_answer = {}

        super().__init__(**kwargs)

    def validate(self):
        """
        Validate this form as usual and check for any form-level validation errors based on question type
        :return: boolean
        """
        valid_fields = FlaskForm.validate(self)
        valid_date_range_form = True
        valid_calculated_form = True
        valid_mutually_exclusive_form = True

        for question in self.schema.get_questions_for_block(self.block_json):
            if question['type'] == 'DateRange' and valid_date_range_form:
                valid_date_range_form = self.validate_date_range_question(question)
            elif question['type'] == 'Calculated' and valid_calculated_form:
                valid_calculated_form = self.validate_calculated_question(question)
            elif question['type'] == 'MutuallyExclusive' and valid_mutually_exclusive_form and valid_fields:
                valid_mutually_exclusive_form = self.validate_mutually_exclusive_question(question)

        return valid_fields and valid_date_range_form and valid_calculated_form and valid_mutually_exclusive_form

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
                self.answers_all_valid([period_from_id, period_to_id])
                and self._validate_date_range_question(question['id'], period_from_id, period_to_id, messages,
                                                       question.get('period_limits'))):
            return False

        return True

    def validate_calculated_question(self, question):
        for calculation in question['calculations']:
            target_total, currency = self._get_target_total_and_currency(calculation, question)
            if (self.answers_all_valid(calculation['answers_to_calculate'])
                    and self._validate_calculated_question(calculation, question, target_total, currency)):
                # Remove any previous question errors if it passes this OR before returning True
                if question['id'] in self.question_errors:
                    self.question_errors.pop(question['id'])
                return True

        return False

    def validate_mutually_exclusive_question(self, question):
        is_mandatory = question.get('mandatory')
        messages = question['validation'].get('messages') if 'validation' in question else None
        answers = (getattr(self, answer['id']).data for answer in question['answers'])

        validator = MutuallyExclusiveCheck(messages=messages)

        try:
            validator(answers, is_mandatory)
        except validators.ValidationError as e:
            self.question_errors[question['id']] = str(e)
            return False

        return True

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

        raise Exception('Invalid calculation_type: {}'.format(calculation_type))

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
                if answer_json['id'] in self.errors:
                    ordered_errors += map_subfield_errors(self.errors, answer_json['id'])
                if 'options' in answer_json:
                    ordered_errors += map_detail_answer_errors(self.errors, answer_json)

        return ordered_errors

    def answer_errors(self, input_id):
        return [error[1] for error in self.map_errors() if input_id == error[0]]

    def get_data(self, answer_id):
        attr = getattr(self, answer_id)
        return attr.raw_data[0] if attr.raw_data else ''


# pylint: disable=too-many-locals
def get_answer_fields(question, data, error_messages, schema, answer_store, metadata):
    answer_fields = {}
    for answer in question.get('answers', []):

        for option in answer.get('options', []):
            disable_validation = False
            if 'detail_answer' in option:
                detail_answer = option['detail_answer']
                detail_answer_error_messages = detail_answer['validation']['messages'] if detail_answer.get('validation') else error_messages
                if isinstance(data, MultiDict):
                    option_value_in_data = option['value'] in data.to_dict(flat=False).get(answer['id'], [])
                else:
                    option_value_in_data = option['value'] in dict(data).get(answer['id'], [])

                if not option_value_in_data:
                    disable_validation = True

                answer_fields[detail_answer['id']] = get_field(detail_answer, detail_answer.get('label'),
                                                               detail_answer_error_messages, answer_store, metadata,
                                                               disable_validation=disable_validation)

        name = answer.get('label') or get_question_title(question, answer_store, schema, metadata)
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


def map_detail_answer_errors(errors, answer_json):
    detail_answer_errors = []

    for option in answer_json['options']:
        if 'detail_answer' in option and option['detail_answer']['id'] in errors:
            for error in errors[option['detail_answer']['id']]:
                detail_answer_errors.append((answer_json['id'], error))

    return detail_answer_errors


def generate_form(schema, block_json, answer_store, metadata, data=None, formdata=None):
    class DynamicForm(QuestionnaireForm):
        pass

    answer_fields = {}
    for question in schema.get_questions_for_block(block_json):
        answer_fields.update(get_answer_fields(
            question,
            formdata if formdata is not None else data,
            schema.error_messages,
            schema,
            answer_store,
            metadata,
        ))

    for answer_id, field in answer_fields.items():
        setattr(DynamicForm, answer_id, field)

    if formdata:
        formdata = MultiDict(formdata)
        formdata = MultiDict(formdata)

    return DynamicForm(schema, block_json, answer_store, metadata, data=data, formdata=formdata)
