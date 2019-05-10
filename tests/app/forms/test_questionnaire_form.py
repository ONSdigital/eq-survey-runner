# pylint: disable=too-many-lines
from decimal import Decimal

from mock import patch

from app.forms.questionnaire_form import generate_form
from app.utilities.schema import load_schema_from_params
from app.validation.validators import ResponseRequired
from app.data_model.answer_store import AnswerStore, Answer

from tests.app.app_context_test_case import AppContextTestCase


class TestQuestionnaireForm(AppContextTestCase):  # noqa: C901  pylint: disable=too-many-public-methods

    @staticmethod
    def _error_exists(answer_id, msg, mapped_errors):
        return any(a_id == answer_id and str(msg) in ordered_errors for a_id, ordered_errors in mapped_errors)

    def test_form_ids_match_block_answer_ids(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'textfield')

            question_schema = schema.get_block('name-block').get('question')

            form = generate_form(schema, question_schema, AnswerStore(), metadata=None)

            for answer_id in schema.get_answer_ids_for_block('name-block'):
                self.assertTrue(hasattr(form, answer_id))

    def test_form_date_range_populates_data(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'date_range')

            question_schema = schema.get_block('date-block').get('question')

            data = {
                'date-range-from-answer-day': '01',
                'date-range-from-answer-month': '3',
                'date-range-from-answer-year': '2016',
                'date-range-to-answer-day': '31',
                'date-range-to-answer-month': '3',
                'date-range-to-answer-year': '2016'
            }

            expected_form_data = {
                'csrf_token': '',
                'date-range-from-answer': '2016-03-01',
                'date-range-to-answer': '2016-03-31'
            }
            form = generate_form(schema, question_schema, AnswerStore(), metadata=None, formdata=data)

            self.assertEqual(form.data, expected_form_data)

    def test_date_range_matching_dates_raises_question_error(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'date_range')

            question_schema = schema.get_block('date-block').get('question')

            data = {
                'date-range-from-answer-day': '25',
                'date-range-from-answer-month': '12',
                'date-range-from-answer-year': '2016',
                'date-range-to-answer-day': '25',
                'date-range-to-answer-month': '12',
                'date-range-to-answer-year': '2016'
            }

            expected_form_data = {
                'csrf_token': '',
                'date-range-from-answer': '2016-12-25',
                'date-range-to-answer': '2016-12-25'
            }
            form = generate_form(schema, question_schema, AnswerStore(), metadata=None, formdata=data)

            form.validate()
            self.assertEqual(form.data, expected_form_data)
            self.assertEqual(form.question_errors['date-range-question'], schema.error_messages
                             ['INVALID_DATE_RANGE'])

    def test_date_range_to_precedes_from_raises_question_error(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'date_range')

            question_schema = schema.get_block('date-block').get('question')

            data = {
                'date-range-from-answer-day': '25',
                'date-range-from-answer-month': '12',
                'date-range-from-answer-year': '2016',
                'date-range-to-answer-day': '24',
                'date-range-to-answer-month': '12',
                'date-range-to-answer-year': '2016'
            }

            expected_form_data = {
                'csrf_token': '',
                'date-range-from-answer': '2016-12-25',
                'date-range-to-answer': '2016-12-24'
            }

            form = generate_form(schema, question_schema, AnswerStore(), metadata=None, formdata=data)

            form.validate()
            self.assertEqual(form.data, expected_form_data)
            self.assertEqual(form.question_errors['date-range-question'], schema.error_messages
                             ['INVALID_DATE_RANGE'], AnswerStore())

    def test_date_range_too_large_period_raises_question_error(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'date_validation_range')

            question_schema = schema.get_block('date-range-block').get('question')

            data = {
                'date-range-from-day': '25',
                'date-range-from-month': '12',
                'date-range-from-year': '2016',
                'date-range-to-day': '24',
                'date-range-to-month': '12',
                'date-range-to-year': '2017'
            }

            expected_form_data = {
                'csrf_token': '',
                'date-range-from': '2016-12-25',
                'date-range-to': '2017-12-24'
            }
            form = generate_form(schema, question_schema, AnswerStore(), metadata=None, formdata=data)

            form.validate()
            self.assertEqual(form.data, expected_form_data)
            self.assertEqual(form.question_errors['date-range-question'], schema.error_messages
                             ['DATE_PERIOD_TOO_LARGE'] % dict(max='1 month, 20 days'), AnswerStore())

    def test_date_range_too_small_period_raises_question_error(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'date_validation_range')

            question_schema = schema.get_block('date-range-block').get('question')

            data = {
                'date-range-from-day': '25',
                'date-range-from-month': '12',
                'date-range-from-year': '2016',
                'date-range-to-day': '26',
                'date-range-to-month': '12',
                'date-range-to-year': '2016'
            }

            expected_form_data = {
                'csrf_token': '',
                'date-range-from': '2016-12-25',
                'date-range-to': '2016-12-26'
            }
            form = generate_form(schema, question_schema, AnswerStore(), metadata=None, formdata=data)

            form.validate()
            self.assertEqual(form.data, expected_form_data)
            self.assertEqual(form.question_errors['date-range-question'], schema.error_messages
                             ['DATE_PERIOD_TOO_SMALL'] % dict(min='23 days'), AnswerStore())

    def test_date_range_valid_period(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'date_validation_range')

            question_schema = schema.get_block('date-range-block')['question']

            data = {
                'date-range-from-day': '25',
                'date-range-from-month': '12',
                'date-range-from-year': '2016',
                'date-range-to-day': '26',
                'date-range-to-month': '01',
                'date-range-to-year': '2017'
            }

            expected_form_data = {
                'csrf_token': '',
                'date-range-from': '2016-12-25',
                'date-range-to': '2017-01-26'
            }
            form = generate_form(schema, question_schema, AnswerStore(), metadata=None, formdata=data)

            form.validate()
            self.assertEqual(form.data, expected_form_data)

    def test_date_combined_single_validation(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'date_validation_combined')

            question_schema = schema.get_block('date-range-block')['question']

            data = {
                'date-range-from-day': '01',
                'date-range-from-month': '1',
                'date-range-from-year': '2017',
                'date-range-to-day': '14',
                'date-range-to-month': '3',
                'date-range-to-year': '2017'
            }

            metadata = {
                'ref_p_start_date': '2017-01-21',
                'ref_p_end_date': '2017-02-21'
            }

            expected_form_data = {
                'csrf_token': '',
                'date-range-from': '2017-01-01',
                'date-range-to': '2017-03-14'
            }
            form = generate_form(schema, question_schema, AnswerStore(), metadata, formdata=data)

            form.validate()
            self.assertEqual(form.data, expected_form_data)
            self.assertEqual(form.errors['date-range-from']['month'][0],
                             schema.error_messages['SINGLE_DATE_PERIOD_TOO_EARLY'] % dict(min='1 January 2017'))

            self.assertEqual(form.errors['date-range-to']['month'][0],
                             schema.error_messages['SINGLE_DATE_PERIOD_TOO_LATE'] % dict(max='14 March 2017'))

    def test_date_combined_range_too_small_validation(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'date_validation_combined')

            question_schema = schema.get_block('date-range-block').get('question')

            data = {
                'date-range-from-day': '01',
                'date-range-from-month': 1,
                'date-range-from-year': '2017',
                'date-range-to-day': '10',
                'date-range-to-month': 1,
                'date-range-to-year': '2017'
            }

            metadata = {
                'ref_p_start_date': '2017-01-20',
                'ref_p_end_date': '2017-02-20'
            }

            expected_form_data = {
                'csrf_token': '',
                'date-range-from': '2017-01-01',
                'date-range-to': '2017-01-10'
            }
            form = generate_form(schema, question_schema, AnswerStore(), metadata, formdata=data)

            form.validate()
            self.assertEqual(form.data, expected_form_data)
            self.assertEqual(form.question_errors['date-range-question'],
                             schema.error_messages['DATE_PERIOD_TOO_SMALL'] % dict(min='10 days'))

    def test_date_combined_range_too_large_validation(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'date_validation_combined')

            question_schema = schema.get_block('date-range-block').get('question')

            data = {
                'date-range-from-day': '01',
                'date-range-from-month': 1,
                'date-range-from-year': '2017',
                'date-range-to-day': '21',
                'date-range-to-month': 2,
                'date-range-to-year': '2017'
            }

            metadata = {
                'ref_p_start_date': '2017-01-20',
                'ref_p_end_date': '2017-02-20'
            }

            expected_form_data = {
                'csrf_token': '',
                'date-range-from': '2017-01-01',
                'date-range-to': '2017-02-21'
            }
            form = generate_form(schema, question_schema, AnswerStore(), metadata, formdata=data)

            form.validate()
            self.assertEqual(form.data, expected_form_data)
            self.assertEqual(form.question_errors['date-range-question'],
                             schema.error_messages['DATE_PERIOD_TOO_LARGE'] % dict(max='50 days'))

    def test_date_mm_yyyy_combined_single_validation(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'date_validation_mm_yyyy_combined')

            question_schema = schema.get_block('date-range-block').get('question')

            data = {
                'date-range-from-month': 11,
                'date-range-from-year': '2016',
                'date-range-to-month': 6,
                'date-range-to-year': '2017'
            }

            metadata = {
                'ref_p_start_date': '2017-01-01',
                'ref_p_end_date': '2017-02-12'
            }

            expected_form_data = {
                'csrf_token': '',
                'date-range-from': '2016-11',
                'date-range-to': '2017-06'
            }
            form = generate_form(schema, question_schema, AnswerStore(), metadata, formdata=data)

            form.validate()
            self.assertEqual(form.data, expected_form_data)
            self.assertEqual(form.errors['date-range-from']['month'][0],
                             schema.error_messages['SINGLE_DATE_PERIOD_TOO_EARLY'] % dict(min='November 2016'))

            self.assertEqual(form.errors['date-range-to']['month'][0],
                             schema.error_messages['SINGLE_DATE_PERIOD_TOO_LATE'] % dict(max='June 2017'))

    def test_date_mm_yyyy_combined_range_too_small_validation(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'date_validation_mm_yyyy_combined')

            question_schema = schema.get_block('date-range-block').get('question')

            data = {
                'date-range-from-month': 1,
                'date-range-from-year': '2017',
                'date-range-to-month': 2,
                'date-range-to-year': '2017'
            }

            metadata = {
                'ref_p_start_date': '2017-01-01',
                'ref_p_end_date': '2017-02-12'
            }

            expected_form_data = {
                'csrf_token': '',
                'date-range-from': '2017-01',
                'date-range-to': '2017-02'
            }
            form = generate_form(schema, question_schema, AnswerStore(), metadata, formdata=data)

            form.validate()
            self.assertEqual(form.data, expected_form_data)
            self.assertEqual(form.question_errors['date-range-question'],
                             schema.error_messages['DATE_PERIOD_TOO_SMALL'] % dict(min='2 months'))

    def test_date_mm_yyyy_combined_range_too_large_validation(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'date_validation_mm_yyyy_combined')

            question_schema = schema.get_block('date-range-block').get('question')

            data = {
                'date-range-from-month': 1,
                'date-range-from-year': '2017',
                'date-range-to-month': 5,
                'date-range-to-year': '2017'
            }

            metadata = {
                'ref_p_start_date': '2017-01-01',
                'ref_p_end_date': '2017-02-12'
            }

            expected_form_data = {
                'csrf_token': '',
                'date-range-from': '2017-01',
                'date-range-to': '2017-05'
            }
            form = generate_form(schema, question_schema, AnswerStore(), metadata, formdata=data)

            form.validate()
            self.assertEqual(form.data, expected_form_data)
            self.assertEqual(form.question_errors['date-range-question'],
                             schema.error_messages['DATE_PERIOD_TOO_LARGE'] % dict(max='3 months'))

    def test_date_yyyy_combined_single_validation(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'date_validation_yyyy_combined')

            question_schema = schema.get_block('date-range-block').get('question')

            data = {'date-range-from-year': '2015', 'date-range-to-year': '2021'}

            metadata = {'ref_p_start_date': '2017-01-01', 'ref_p_end_date': '2017-02-12'}

            expected_form_data = {
                'csrf_token': '',
                'date-range-from': '2015',
                'date-range-to': '2021'
            }
            form = generate_form(schema, question_schema, AnswerStore(), metadata, formdata=data)

            form.validate()
            self.assertEqual(form.data, expected_form_data)
            self.assertEqual(form.errors['date-range-from']['year'][0],
                             schema.error_messages['SINGLE_DATE_PERIOD_TOO_EARLY'] % dict(min='2015'))

            self.assertEqual(form.errors['date-range-to']['year'][0],
                             schema.error_messages['SINGLE_DATE_PERIOD_TOO_LATE'] % dict(max='2021'))

    def test_date_yyyy_combined_range_too_small_validation(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'date_validation_yyyy_combined')

            question_schema = schema.get_block('date-range-block').get('question')

            data = {'date-range-from-year': '2016', 'date-range-to-year': '2017'}

            metadata = {'ref_p_start_date': '2017-01-01', 'ref_p_end_date': '2017-02-12'}

            expected_form_data = {
                'csrf_token': '',
                'date-range-from': '2016',
                'date-range-to': '2017'
            }
            form = generate_form(schema, question_schema, AnswerStore(), metadata, formdata=data)

            form.validate()
            self.assertEqual(form.data, expected_form_data)
            self.assertEqual(form.question_errors['date-range-question'],
                             schema.error_messages['DATE_PERIOD_TOO_SMALL'] % dict(min='2 years'))

    def test_date_yyyy_combined_range_too_large_validation(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'date_validation_yyyy_combined')

            question_schema = schema.get_block('date-range-block').get('question')

            data = {'date-range-from-year': '2016', 'date-range-to-year': '2020'}

            metadata = {'ref_p_start_date': '2017-01-01', 'ref_p_end_date': '2017-02-12'}

            expected_form_data = {
                'csrf_token': '',
                'date-range-from': '2016',
                'date-range-to': '2020'
            }
            form = generate_form(schema, question_schema, AnswerStore(), metadata, formdata=data)

            form.validate()
            self.assertEqual(form.data, expected_form_data)
            self.assertEqual(form.question_errors['date-range-question'],
                             schema.error_messages['DATE_PERIOD_TOO_LARGE'] % dict(max='3 years'))

    def test_bespoke_message_for_date_validation_range(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'date_validation_range')

            question_schema = schema.get_block('date-range-block').get('question')

            question_schema = {
                'id': 'date-range-question',
                'type': 'DateRange',
                'validation': {
                    'messages': {
                        'DATE_PERIOD_TOO_SMALL': 'Test Message'
                    }
                },
                'period_limits': {
                    'minimum': {
                        'days': 20
                    }
                },
                'answers': [{
                    'id': 'date-range-from',
                    'label': 'Period from',
                    'mandatory': True,
                    'type': 'Date'
                }, {
                    'id': 'date-range-to',
                    'label': 'Period to',
                    'mandatory': True,
                    'type': 'Date'
                }]
            }

            data = {
                'date-range-from-day': '25',
                'date-range-from-month': '1',
                'date-range-from-year': '2018',
                'date-range-to-day': '26',
                'date-range-to-month': '1',
                'date-range-to-year': '2018'
            }

            form = generate_form(schema, question_schema, AnswerStore(), metadata=None, formdata=data)

            with patch('app.questionnaire.questionnaire_schema.QuestionnaireSchema.get_all_questions_for_block',
                       return_value=[question_schema]):
                form.validate()
                self.assertIn(form.question_errors['date-range-question'], 'Test Message')

    def test_invalid_minimum_period_limit_and_single_date_periods(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'date_validation_range')

            question_schema = schema.get_block('date-range-block')['question']

            question_schema = {
                'id': 'date-range-question',
                'type': 'DateRange',
                'period_limits': {
                    'minimum': {
                        'months': 2
                    }
                },
                'answers': [{
                    'id': 'date-range-from',
                    'label': 'Period from',
                    'mandatory': True,
                    'type': 'Date',
                    'minimum': {
                        'value': '2018-01-10',
                        'offset_by': {
                            'days': -5
                        }
                    }
                }, {
                    'id': 'date-range-to',
                    'label': 'Period to',
                    'mandatory': True,
                    'type': 'Date',
                    'maximum': {
                        'value': '2018-01-10',
                        'offset_by': {
                            'days': 5
                        }
                    }
                }]
            }

            data = {
                'date-range-from-day': '8',
                'date-range-from-month': '1',
                'date-range-from-year': '2018',
                'date-range-to-day': '13',
                'date-range-to-month': '1',
                'date-range-to-year': '2018'
            }

            form = generate_form(schema, question_schema, AnswerStore(), metadata=None, formdata=data)

            with self.assertRaises(Exception) as ite:
                with patch('app.questionnaire.questionnaire_schema.QuestionnaireSchema.get_all_questions_for_block',
                           return_value=[question_schema]):
                    form.validate()
                    self.assertEqual('The schema has invalid period_limits for date-range-question', str(ite.exception))

    def test_invalid_maximum_period_limit_and_single_date_periods(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'date_validation_range')

            question_schema = schema.get_block('date-range-block').get('question')

            question_schema = {
                'id': 'date-range-question',
                'type': 'DateRange',
                'period_limits': {
                    'maximum': {
                        'days': 8
                    }
                },
                'answers': [{
                    'id': 'date-range-from',
                    'label': 'Period from',
                    'mandatory': True,
                    'type': 'Date',
                    'minimum': {
                        'value': '2018-01-10',
                        'offset_by': {
                            'days': -5
                        }
                    }
                }, {
                    'id': 'date-range-to',
                    'label': 'Period to',
                    'mandatory': True,
                    'type': 'Date',
                    'maximum': {
                        'value': '2018-01-10',
                        'offset_by': {
                            'days': 5
                        }
                    }
                }]
            }

            data = {
                'date-range-from-day': '6',
                'date-range-from-month': '1',
                'date-range-from-year': '2018',
                'date-range-to-day': '15',
                'date-range-to-month': '1',
                'date-range-to-year': '2018'
            }

            form = generate_form(schema, question_schema, AnswerStore(), metadata=None, formdata=data)

            with self.assertRaises(Exception) as ite:
                with patch('app.questionnaire.questionnaire_schema.QuestionnaireSchema.get_all_questions_for_block',
                           return_value=[question_schema]):
                    form.validate()
                    self.assertEqual('The schema has invalid period_limits for date-range-question', str(ite.exception))

    def test_invalid_date_range_and_single_date_periods(self):
        with self.app_request_context():
            store = AnswerStore()
            test_answer_id = Answer(
                answer_id='date',
                value='2017-03-20',
            )
            store.add_or_update(test_answer_id)

            schema = load_schema_from_params('test', 'date_validation_range')

            question_schema = schema.get_block('date-range-block').get('question')

            question_schema = {
                'id': 'date-range-question',
                'type': 'DateRange',
                'answers': [{
                    'id': 'date-range-from',
                    'label': 'Period from',
                    'mandatory': True,
                    'type': 'Date',
                    'minimum': {
                        'value': '2018-01-10',
                        'offset_by': {
                            'days': -5
                        }
                    }
                }, {
                    'id': 'date-range-to',
                    'label': 'Period to',
                    'mandatory': True,
                    'type': 'Date',
                    'maximum': {
                        'answer_id': 'date',
                        'offset_by': {
                            'days': 5
                        }
                    }
                }]
            }

            data = {
                'date-range-from-day': '6',
                'date-range-from-month': '1',
                'date-range-from-year': '2018',
                'date-range-to-day': '15',
                'date-range-to-month': '1',
                'date-range-to-year': '2018'
            }

            metadata = {
                'eq_id': 'test',
                'form_type': 'date_validation_range'
            }

            form = generate_form(schema, question_schema, store, metadata=metadata, formdata=data)


            with self.assertRaises(Exception) as ite:
                with patch('app.questionnaire.questionnaire_schema.QuestionnaireSchema.get_all_questions_for_block', return_value=[question_schema]):
                    form.validate()
                    self.assertEqual('The schema has invalid date answer limits for date-range-question', str(ite.exception))

    def test_invalid_calculation_type(self):
        store = AnswerStore()

        answer_total = Answer(
            answer_id='total-answer',
            value=10,
        )

        store.add_or_update(answer_total)

        with self.app_request_context():
            schema = load_schema_from_params('test', 'sum_equal_validation_against_total')

            question_schema = schema.get_block('breakdown-block').get('question')

            question_schema['calculations'] = [{
                'calculation_type': 'subtraction',
                'answer_id': 'total-answer',
                'answers_to_calculate': [
                    'breakdown-1',
                    'breakdown-2'
                ],
                'conditions': [
                    'equals'
                ]
            }]

            data = {
                'breakdown-1': '3',
                'breakdown-2': '5',
            }

            form = generate_form(schema, question_schema, store, metadata=None, formdata=data)

            with self.assertRaises(Exception) as ite:
                with patch('app.questionnaire.questionnaire_schema.QuestionnaireSchema.get_all_questions_for_block',
                           return_value=[question_schema]):
                    form.validate()
            self.assertEqual('Invalid calculation_type: subtraction', str(ite.exception))

    def test_bespoke_message_for_sum_validation(self):
        store = AnswerStore()

        answer_total = Answer(
            answer_id='total-answer',
            value=10,
        )

        store.add_or_update(answer_total)

        with self.app_request_context():
            schema = load_schema_from_params('test', 'sum_equal_validation_against_total')

            question_schema = schema.get_block('breakdown-block').get('question')

            question_schema['validation'] = {
                'messages': {
                    'TOTAL_SUM_NOT_EQUALS': 'Test Message'
                }
            }

            data = {
                'breakdown-1': '3',
                'breakdown-2': '5',
            }

            form = generate_form(schema, question_schema, store, metadata=None, formdata=data)

            with patch('app.questionnaire.questionnaire_schema.QuestionnaireSchema.get_all_questions_for_block',
                       return_value=[question_schema]):
                form.validate()
                self.assertIn(form.question_errors['breakdown-question'], 'Test Message')

    def test_empty_calculated_field(self):
        store = AnswerStore()

        answer_total = Answer(
            answer_id='total-answer',
            value=10,
        )

        store.add_or_update(answer_total)

        with self.app_request_context():
            schema = load_schema_from_params('test', 'sum_equal_validation_against_total')

            question_schema = schema.get_block('breakdown-block').get('question')

            data = {
                'breakdown-1': '',
                'breakdown-2': '5',
                'breakdown-3': '4',
                'breakdown-4': ''
            }

            expected_form_data = {
                'csrf_token': '',
                'breakdown-1': None,
                'breakdown-2': Decimal('5'),
                'breakdown-3': Decimal('4'),
                'breakdown-4': None
            }
            form = generate_form(schema, question_schema, store, metadata=None, formdata=data)

            form.validate()
            self.assertEqual(form.data, expected_form_data)
            self.assertEqual(form.question_errors['breakdown-question'], schema.error_messages['TOTAL_SUM_NOT_EQUALS']
                             % dict(total='10'), AnswerStore())

    def test_sum_calculated_field(self):
        store = AnswerStore()

        answer_total = Answer(
            answer_id='total-answer',
            value=10,
        )

        store.add_or_update(answer_total)

        with self.app_request_context():
            schema = load_schema_from_params('test', 'sum_equal_validation_against_total')

            question_schema = schema.get_block('breakdown-block').get('question')

            data = {
                'breakdown-1': '',
                'breakdown-2': '5',
                'breakdown-3': '4',
                'breakdown-4': '1'
            }

            expected_form_data = {
                'csrf_token': '',
                'breakdown-1': None,
                'breakdown-2': Decimal('5'),
                'breakdown-3': Decimal('4'),
                'breakdown-4': Decimal('1')
            }
            form = generate_form(schema, question_schema, store, metadata=None, formdata=data)

            form.validate()
            self.assertEqual(form.data, expected_form_data)

    def test_get_calculation_total_with_no_input(self):
        store = AnswerStore()

        answer_total = Answer(
            answer_id='total-answer',
            value=10,
        )

        store.add_or_update(answer_total)

        with self.app_request_context():
            schema = load_schema_from_params('test', 'sum_equal_validation_against_total')

            question_schema = schema.get_block('breakdown-block').get('question')

            data = {
                'breakdown-1': '',
                'breakdown-2': '',
                'breakdown-3': '',
                'breakdown-4': ''
            }

            expected_form_data = {
                'csrf_token': '',
                'breakdown-1': None,
                'breakdown-2': None,
                'breakdown-3': None,
                'breakdown-4': None
            }
            form = generate_form(schema, question_schema, store, metadata=None, formdata=data)

            form.validate()
            self.assertEqual(form.data, expected_form_data)
            self.assertEqual(form.question_errors['breakdown-question'], schema.error_messages['TOTAL_SUM_NOT_EQUALS']
                             % dict(total='10'), AnswerStore())

    def test_multi_calculation(self):
        store = AnswerStore()

        answer_total = Answer(
            answer_id='total-answer',
            value=10,
        )

        store.add_or_update(answer_total)

        with self.app_request_context():
            schema = load_schema_from_params('test', 'sum_multi_validation_against_total')

            question_schema = schema.get_block('breakdown-block').get('question')

            data = {
                'breakdown-1': '',
                'breakdown-2': '',
                'breakdown-3': '',
                'breakdown-4': ''
            }

            # With no answers question validation should pass
            form = generate_form(schema, question_schema, store, metadata=None, formdata=data)
            form.validate()

            self.assertEqual(len(form.question_errors), 0)

            # With the data equaling the total question validation should pass
            data['breakdown-1'] = '10'

            form = generate_form(schema, question_schema, store, metadata=None, formdata=data)
            form.validate()

            self.assertEqual(len(form.question_errors), 0)

            # With the data not equaling zero or the total, question validation should fail
            data['breakdown-1'] = '1'

            form = generate_form(schema, question_schema, store, metadata=None, formdata=data)
            form.validate()

            self.assertEqual(form.question_errors['breakdown-question'],
                             schema.error_messages['TOTAL_SUM_NOT_EQUALS'] % dict(total='10'))

    def test_generate_form_with_title_and_no_answer_label(self):
        """
        Checks that the form is still generated when there is no answer label but there is a question title
        """
        store = AnswerStore()

        conditional_answer = Answer(
            answer_id='behalf-of-answer',
            value='chad',
        )

        store.add_or_update(conditional_answer)

        with self.app_request_context():
            schema = load_schema_from_params('test', 'title')

            question_schema = schema.get_block('single-title-block').get('question')

            data = {
                'feeling-answer': 'good'
            }

            expected_form_data = {
                'csrf_token': '',
                'feeling-answer': 'good'
            }

            with patch('app.questionnaire.path_finder.evaluate_goto', return_value=False):
                form = generate_form(schema, question_schema, store, metadata={}, formdata=data)

            form.validate()
            assert form.data == expected_form_data

    def test_form_errors_are_correctly_mapped(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'numbers')

            question_schema = schema.get_block('set-min-max-block').get('question')

            form = generate_form(schema, question_schema, AnswerStore(), metadata=None)

            form.validate()
            mapped_errors = form.map_errors()

            self.assertTrue(self._error_exists('set-minimum',
                                               schema.error_messages['MANDATORY_NUMBER'],
                                               mapped_errors))

    def test_form_subfield_errors_are_correctly_mapped(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'date_range')

            question_schema = schema.get_block('date-block').get('question')

            form = generate_form(schema, question_schema, AnswerStore(), metadata=None)

            form.validate()
            mapped_errors = form.map_errors()

            self.assertTrue(self._error_exists('date-range-from-answer', schema.error_messages['MANDATORY_DATE'], mapped_errors))
            self.assertTrue(self._error_exists('date-range-to-answer', schema.error_messages['MANDATORY_DATE'], mapped_errors))

    def test_detail_answer_mandatory_only_checked_if_option_selected(self):
        # The detail_answer can only be mandatory if the option it is associated with is answered
        with self.app_request_context():
            schema = load_schema_from_params('test', 'checkbox_multiple_detail_answers')

            question_schema = schema.get_block('mandatory-checkbox').get('question')

            #  Option is selected therefore the detail answer should be mandatory (schema defined)
            form = generate_form(schema, question_schema, AnswerStore(), metadata=None, formdata={
                'mandatory-checkbox-answer': 'Your choice'
            })

            detail_answer_field = getattr(form, 'your-choice-answer-mandatory')
            self.assertIsInstance(detail_answer_field.validators[0], ResponseRequired)

            #  Option not selected therefore the detail answer should not be mandatory
            form = generate_form(schema, question_schema, AnswerStore(), metadata=None, formdata={'mandatory-checkbox-answer': 'Ham'})

            detail_answer_field = getattr(form, 'your-choice-answer-mandatory')
            self.assertEqual(detail_answer_field.validators, [])

    def test_answer_with_detail_answer_errors_are_correctly_mapped(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'radio_mandatory_with_mandatory_other')

            question_schema = schema.get_block('radio-mandatory').get('question')

            form = generate_form(schema, question_schema, AnswerStore(), metadata=None, formdata={
                'radio-mandatory-answer': 'Other'
            })

            form.validate()
            mapped_errors = form.map_errors()

            self.assertTrue(self._error_exists('radio-mandatory-answer', schema.error_messages['MANDATORY_TEXTFIELD'],
                                               mapped_errors))
            self.assertFalse(self._error_exists('other-answer-mandatory', schema.error_messages['MANDATORY_TEXTFIELD'],
                                                mapped_errors))

    def test_answer_errors_are_interpolated(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'numbers')

            question_schema = schema.get_block('set-min-max-block').get('question')

            form = generate_form(schema, question_schema, AnswerStore(), metadata=None, formdata={
                'set-minimum': '-1'
            })

            form.validate()
            answer_errors = form.answer_errors('set-minimum')
            self.assertIn(schema.error_messages['NUMBER_TOO_SMALL'] % dict(min='0'), answer_errors)

    def test_mandatory_mutually_exclusive_question_raises_error_when_not_answered(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'mutually_exclusive')

            question_schema = schema.get_block('mutually-exclusive-checkbox').get('question')

            form = generate_form(schema, question_schema, AnswerStore(), metadata=None, formdata={})
            form.validate_mutually_exclusive_question(question_schema)

            self.assertEqual(form.question_errors['mutually-exclusive-checkbox-question'], 'Enter an answer to continue.')

    def test_mutually_exclusive_question_raises_error_when_both_answered(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'mutually_exclusive')

            question_schema = schema.get_block('mutually-exclusive-date').get('question')

            data = {
                'date-answer-day': '17',
                'date-answer-month': '9',
                'date-answer-year': '2018',
                'date-exclusive-answer': 'I prefer not to say',
            }

            form = generate_form(schema, question_schema, AnswerStore(), metadata=None, formdata=data)
            form.validate_mutually_exclusive_question(question_schema)

            self.assertEqual(form.question_errors['mutually-exclusive-date-question'], 'Remove an answer to continue.')
