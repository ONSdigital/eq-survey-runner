from datetime import datetime

from dateutil.relativedelta import relativedelta
from mock import patch
from wtforms import Form

from app.data_model.answer_store import AnswerStore, Answer
from app.forms.date_form import get_date_form, get_month_year_form, get_year_form, \
    get_referenced_offset_value, get_dates_for_single_date_period_validation, \
    validate_mandatory_date, DateField, MonthYearField, YearField
from app.questionnaire.rules import convert_to_datetime
from app.utilities.schema import load_schema_from_params
from tests.app.app_context_test_case import AppContextTestCase


class TestDateForm(AppContextTestCase):

    def test_generate_date_form_creates_empty_form(self):
        schema = load_schema_from_params('test', 'dates')
        error_messages = schema.error_messages

        with self.app_request_context('/'):
            form = get_date_form(AnswerStore(), {}, schema.get_answers('single-date-answer')[0], error_messages=error_messages)

        self.assertTrue(hasattr(form, 'day'))
        self.assertTrue(hasattr(form, 'month'))
        self.assertTrue(hasattr(form, 'year'))

    def test_generate_month_year_date_form_creates_empty_form(self):
        schema = load_schema_from_params('test', 'dates')
        error_messages = schema.error_messages


        with self.app_request_context('/'):
            form = get_month_year_form(schema.get_answers('month-year-answer')[0], {}, {}, error_messages=error_messages)

        self.assertFalse(hasattr(form, 'day'))
        self.assertTrue(hasattr(form, 'month'))
        self.assertTrue(hasattr(form, 'year'))

    def test_generate_year_date_form_creates_empty_form(self):
        schema = load_schema_from_params('test', 'dates')
        error_messages = schema.error_messages

        form = get_year_form(schema.get_answers('year-date-answer')[0], {}, {}, error_messages=error_messages, label=None, guidance=None)

        self.assertFalse(hasattr(form, 'day'))
        self.assertFalse(hasattr(form, 'month'))
        self.assertTrue(hasattr(form, 'year'))

    def test_date_form_empty_data(self):
        schema = load_schema_from_params('test', 'dates')
        error_messages = schema.error_messages


        with self.app_request_context('/'):
            form = get_date_form(AnswerStore(), {}, schema.get_answers('single-date-answer')[0], error_messages=error_messages)

        self.assertIsNone(form().data)

    def test_month_year_date_form_empty_data(self):
        schema = load_schema_from_params('test', 'dates')
        error_messages = schema.error_messages

        with self.app_request_context('/'):
            form = get_month_year_form(schema.get_answers('month-year-answer')[0], {}, {}, error_messages=error_messages)

        self.assertIsNone(form().data)

    def test_year_date_form_empty_data(self):
        schema = load_schema_from_params('test', 'dates')
        error_messages = schema.error_messages

        form = get_year_form(schema.get_answers('year-date-answer')[0], {}, {}, error_messages=error_messages, label=None, guidance=None)

        self.assertIsNone(form().data)

    def test_date_form_format_data(self):
        schema = load_schema_from_params('test', 'dates')
        error_messages = schema.error_messages

        data = {'field': '2000-01-01'}

        with self.app_request_context('/'):
            class TestForm(Form):
                field = DateField(AnswerStore(), {}, schema.get_answers('single-date-answer')[0], error_messages)

            test_form = TestForm(data=data)

        self.assertEqual(test_form.field.data, '2000-01-01')

    def test_month_year_date_form_format_data(self):
        schema = load_schema_from_params('test', 'dates')
        error_messages = schema.error_messages

        data = {'field': '2000-01'}

        with self.app_request_context('/'):
            class TestForm(Form):
                field = MonthYearField(schema.get_answers('month-year-answer')[0], {}, {}, error_messages)

            test_form = TestForm(data=data)

        self.assertEqual(test_form.field.data, '2000-01')

    def test_year_date_form_format_data(self):
        schema = load_schema_from_params('test', 'dates')
        error_messages = schema.error_messages

        data = {'field': '2000'}

        class TestForm(Form):
            field = YearField(schema.get_answers('year-date-answer')[0], {}, {}, error_messages)

        test_form = TestForm(data=data)

        self.assertEqual(test_form.field.data, '2000')

    def test_generate_date_form_validates_single_date_period(self):
        schema = load_schema_from_params('test', 'date_validation_single')
        error_messages = schema.error_messages
        test_metadata = {'ref_p_start_date': '2017-02-20'}

        with self.app_request_context('/'):
            form = get_date_form(AnswerStore(), test_metadata, schema.get_answers('date-range-from')[0], error_messages=error_messages)

        self.assertTrue(hasattr(form, 'day'))
        self.assertTrue(hasattr(form, 'month'))
        self.assertTrue(hasattr(form, 'year'))

    def test_generate_date_form_validates_single_date_period_with_bespoke_message(self):
        schema = load_schema_from_params('test', 'date_validation_single')
        error_messages = schema.error_messages
        answer = {
            'id': 'date-range-from',
            'mandatory': True,
            'label': 'Period from',
            'type': 'Date',
            'maximum': {
                'value': '2017-06-11',
                'offset_by': {
                    'days': 20
                }
            },
            'validation': {
                'messages': {
                    'SINGLE_DATE_PERIOD_TOO_LATE': 'Test Message'
                }
            }
        }

        with patch('app.questionnaire.questionnaire_schema.QuestionnaireSchema.get_answers',
                   return_value=[answer]), self.app_request_context('/'):
            form = get_date_form(AnswerStore(), {}, answer, error_messages=error_messages)

            self.assertTrue(hasattr(form, 'day'))
            self.assertTrue(hasattr(form, 'month'))
            self.assertTrue(hasattr(form, 'year'))

    def test_get_referenced_offset_value_for_value(self):
        answer_minimum = {
            'value': '2017-06-11',
            'offset_by': {
                'days': 10
            }
        }

        value = get_referenced_offset_value(answer_minimum, AnswerStore(), {})

        self.assertEqual(value, convert_to_datetime('2017-06-21'))

    def test_get_referenced_offset_value_for_now_value(self):
        answer_minimum = {
            'value': 'now',
            'offset_by': {
                'days': 10
            }
        }

        value = get_referenced_offset_value(answer_minimum, AnswerStore(), {})

        self.assertEqual(datetime.date(value), (datetime.now().date() + relativedelta(days=10)))

    def test_get_referenced_offset_value_for_meta(self):
        test_metadata = {'date': '2018-02-20'}
        answer_minimum = {
            'meta': 'date',
            'offset_by': {
                'days': -10
            }
        }

        value = get_referenced_offset_value(answer_minimum, AnswerStore(), test_metadata)

        self.assertEqual(value, convert_to_datetime('2018-02-10'))

    # pylint: disable=unused-argument
    @patch('app.forms.date_form.load_schema_from_metadata')
    def test_get_referenced_offset_value_for_answer_id(self, mock1):
        store = AnswerStore()

        test_answer_id = Answer(
            answer_id='date',
            value='2018-03-20',
        )
        store.add_or_update(test_answer_id)

        answer_maximum = {
            'answer_id': 'date',
            'offset_by': {
                'months': 1
            }
        }

        value = get_referenced_offset_value(answer_maximum, store, {})

        self.assertEqual(value, convert_to_datetime('2018-04-20'))

    def test_get_referenced_offset_value_with_no_offset(self):
        answer_minimum = {
            'value': '2017-06-11',
        }

        value = get_referenced_offset_value(answer_minimum, AnswerStore(), {})

        self.assertEqual(value, convert_to_datetime('2017-06-11'))

    # pylint: disable=unused-argument
    @patch('app.forms.date_form.load_schema_from_metadata')
    def test_minimum_and_maximum_offset_dates(self, mock1):
        test_metadata = {'date': '2018-02-20'}
        store = AnswerStore()

        test_answer_id = Answer(
            answer_id='date',
            value='2018-03-20',
        )
        store.add_or_update(test_answer_id)

        answer = {
            'id': 'date_answer',
            'type': 'Date',
            'minimum': {
                'meta': 'date',
                'offset_by': {
                    'days': -10
                }
            },
            'maximum': {
                'answer_id': 'date',
                'offset_by': {
                    'years': 1
                }
            }
        }

        offset_dates = get_dates_for_single_date_period_validation(answer, store, metadata=test_metadata)

        self.assertEqual(offset_dates, (convert_to_datetime('2018-02-10'), convert_to_datetime('2019-03-20')))

    def test_greater_minimum_date_than_maximum_date(self):
        answer = {
            'id': 'date_answer',
            'type': 'Date',
            'minimum': {
                'value': '2018-02-15',
                'offset_by': {
                    'days': -10
                }
            },
            'maximum': {
                'value': '2018-01-15',
                'offset_by': {
                    'days': 10
                }
            }
        }

        with self.assertRaises(Exception) as ite:
            get_dates_for_single_date_period_validation(answer, AnswerStore(), {})
            self.assertEqual('The minimum offset date is greater than the maximum offset date for date-answer.',
                             str(ite.exception))

    def test_validate_mandatory_date(self):
        schema = load_schema_from_params('test', 'date_validation_single')
        error_messages = schema.error_messages
        answer = {
            'id': 'date-range-from',
            'mandatory': True,
            'label': 'Period from',
            'type': 'Date',
            'maximum': {
                'value': '2017-06-11',
                'offset_by': {
                    'days': 20
                }
            },
            'validation': {
                'messages': {
                    'MANDATORY_DATE': 'Test Mandatory Date Message'
                }
            }
        }
        validator = validate_mandatory_date(error_messages, answer)
        self.assertEqual(validator[0].message, 'Test Mandatory Date Message')
