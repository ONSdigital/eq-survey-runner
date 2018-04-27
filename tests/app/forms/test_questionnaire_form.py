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
        return any(a_id == answer_id and msg in ordered_errors for a_id, ordered_errors in mapped_errors)

    def test_form_ids_match_block_answer_ids(self):
        with self.test_request_context():
            schema = load_schema_from_params('test', '0102')

            block_json = schema.get_block('reporting-period')

            form = generate_form(schema, block_json, {}, AnswerStore(), metadata=None)

            for answer in schema.get_answers_for_block('reporting-period'):
                self.assertTrue(hasattr(form, answer['id']))

    def test_form_date_range_populates_data(self):
        with self.test_request_context():
            schema = load_schema_from_params('test', '0102')

            block_json = schema.get_block('reporting-period')

            data = {
                'period-from-day': '01',
                'period-from-month': '3',
                'period-from-year': '2016',
                'period-to-day': '31',
                'period-to-month': '3',
                'period-to-year': '2016'
            }

            expected_form_data = {
                'csrf_token': '',
                'period-from': {'day': '01', 'month': '3', 'year': '2016'},
                'period-to': {'day': '31', 'month': '3', 'year': '2016'}
            }
            form = generate_form(schema, block_json, data, AnswerStore(), metadata=None)

            self.assertEqual(form.data, expected_form_data)

    def test_date_range_matching_dates_raises_question_error(self):
        with self.test_request_context():
            schema = load_schema_from_params('test', '0102')

            block_json = schema.get_block('reporting-period')

            data = {
                'period-from-day': '25',
                'period-from-month': '12',
                'period-from-year': '2016',
                'period-to-day': '25',
                'period-to-month': '12',
                'period-to-year': '2016'
            }

            expected_form_data = {
                'csrf_token': '',
                'period-from': {'day': '25', 'month': '12', 'year': '2016'},
                'period-to': {'day': '25', 'month': '12', 'year': '2016'}
            }
            form = generate_form(schema, block_json, data, AnswerStore(), metadata=None)

            form.validate()
            self.assertEqual(form.data, expected_form_data)
            self.assertEqual(form.question_errors['reporting-period-question'], schema.error_messages
                             ['INVALID_DATE_RANGE'])

    def test_date_range_to_precedes_from_raises_question_error(self):
        with self.test_request_context():
            schema = load_schema_from_params('test', '0102')

            block_json = schema.get_block('reporting-period')

            data = {
                'period-from-day': '25',
                'period-from-month': '12',
                'period-from-year': '2016',
                'period-to-day': '24',
                'period-to-month': '12',
                'period-to-year': '2016'
            }

            expected_form_data = {
                'csrf_token': '',
                'period-from': {'day': '25', 'month': '12', 'year': '2016'},
                'period-to': {'day': '24', 'month': '12', 'year': '2016'}
            }
            form = generate_form(schema, block_json, data, AnswerStore(), metadata=None)

            form.validate()
            self.assertEqual(form.data, expected_form_data)
            self.assertEqual(form.question_errors['reporting-period-question'], schema.error_messages
                             ['INVALID_DATE_RANGE'], AnswerStore())

    def test_date_range_too_large_period_raises_question_error(self):
        with self.test_request_context():
            schema = load_schema_from_params('test', 'date_range_period_validation')

            block_json = schema.get_block('date-range-block')

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
                'date-range-from': {'day': '25', 'month': '12', 'year': '2016'},
                'date-range-to': {'day': '24', 'month': '12', 'year': '2017'}
            }
            form = generate_form(schema, block_json, data, AnswerStore(), metadata=None)

            form.validate()
            self.assertEqual(form.data, expected_form_data)
            self.assertEqual(form.question_errors['date-range-question'], schema.error_messages
                             ['DATE_PERIOD_TOO_LARGE'] % dict(max='1 month, 20 days'), AnswerStore())

    def test_date_range_too_small_period_raises_question_error(self):
        with self.test_request_context():
            schema = load_schema_from_params('test', 'date_range_period_validation')

            block_json = schema.get_block('date-range-block')

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
                'date-range-from': {'day': '25', 'month': '12', 'year': '2016'},
                'date-range-to': {'day': '26', 'month': '12', 'year': '2016'}
            }
            form = generate_form(schema, block_json, data, AnswerStore(), metadata=None)

            form.validate()
            self.assertEqual(form.data, expected_form_data)
            self.assertEqual(form.question_errors['date-range-question'], schema.error_messages
                             ['DATE_PERIOD_TOO_SMALL'] % dict(min='23 days'), AnswerStore())

    def test_date_range_valid_period(self):
        with self.test_request_context():
            schema = load_schema_from_params('test', 'date_range_period_validation')

            block_json = schema.get_block('date-range-block')

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
                'date-range-from': {'day': '25', 'month': '12', 'year': '2016'},
                'date-range-to': {'day': '26', 'month': '01', 'year': '2017'}
            }
            form = generate_form(schema, block_json, data, AnswerStore(), metadata=None)

            form.validate()
            self.assertEqual(form.data, expected_form_data)

    def test_bespoke_message_for_date_range_period_validation(self):
        with self.test_request_context():
            schema = load_schema_from_params('test', 'date_range_period_validation')

            block_json = schema.get_block('date-range-block')

            question_json = {
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

            form = generate_form(schema, block_json, data, AnswerStore(), metadata=None)

            with patch('app.questionnaire.questionnaire_schema.QuestionnaireSchema.get_questions_for_block',
                       return_value=[question_json]):
                form.validate()
                self.assertIn(form.question_errors['date-range-question'], 'Test Message')

    def test_invalid_minimum_period_limit_and_single_date_periods(self):
        with self.test_request_context():
            schema = load_schema_from_params('test', 'date_range_period_validation')

            block_json = schema.get_block('date-range-block')

            question_json = {
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

            form = generate_form(schema, block_json, data, AnswerStore(), metadata=None)

            with self.assertRaises(Exception) as ite:
                with patch('app.questionnaire.questionnaire_schema.QuestionnaireSchema.get_questions_for_block',
                           return_value=[question_json]):
                    form.validate()
                    self.assertEqual('The schema has invalid period_limits for date-range-question', str(ite.exception))

    def test_invalid_maximum_period_limit_and_single_date_periods(self):
        with self.test_request_context():
            schema = load_schema_from_params('test', 'date_range_period_validation')

            block_json = schema.get_block('date-range-block')

            question_json = {
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

            form = generate_form(schema, block_json, data, AnswerStore(), metadata=None)

            with self.assertRaises(Exception) as ite:
                with patch('app.questionnaire.questionnaire_schema.QuestionnaireSchema.get_questions_for_block',
                           return_value=[question_json]):
                    form.validate()
                    self.assertEqual('The schema has invalid period_limits for date-range-question', str(ite.exception))

    def test_invalid_date_range_and_single_date_periods(self):
        with self.test_request_context():
            store = AnswerStore()
            test_answer_id = Answer(
                answer_id='date',
                answer_instance=1,
                group_instance=0,
                value='2017-03-20',
            )
            store.add(test_answer_id)

            schema = load_schema_from_params('test', 'date_range_period_validation')

            block_json = schema.get_block('date-range-block')

            question_json = {
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

            form = generate_form(schema, block_json, data, store, metadata=None)

            with self.assertRaises(Exception) as ite:
                with patch('app.questionnaire.questionnaire_schema.QuestionnaireSchema.get_questions_for_block',
                           return_value=[question_json]):
                    form.validate()
                    self.assertEqual('The schema has invalid date answer limits for date-range-question', str(ite.exception))

    def test_invalid_calculation_type(self):
        store = AnswerStore()

        answer_total = Answer(
            answer_id='total-answer',
            answer_instance=1,
            group_instance=1,
            value=10,
        )

        store.add(answer_total)

        with self.test_request_context():
            schema = load_schema_from_params('test', 'sum_equal_validation_against_total')

            block_json = schema.get_block('breakdown-block')

            question_json = {
                'id': 'breakdown-question',
                'type': 'Calculated',
                'calculations': [{
                    'calculation_type': 'subtraction',
                    'answer_id': 'total-answer',
                    'answers_to_calculate': [
                        'breakdown-1',
                        'breakdown-2'
                    ],
                    'conditions': [
                        'equals'
                    ]
                }],
                'answers': [{
                    'id': 'breakdown-1',
                    'label': 'Breakdown 1',
                    'type': 'Number'
                }, {
                    'id': 'breakdown-2',
                    'label': 'Breakdown 2',
                    'type': 'Number'
                }]
            }

            data = {
                'breakdown-1': '3',
                'breakdown-2': '5',
            }

            form = generate_form(schema, block_json, data, store, metadata=None)

            with self.assertRaises(Exception) as ite:
                with patch('app.questionnaire.questionnaire_schema.QuestionnaireSchema.get_questions_for_block',
                           return_value=[question_json]):
                    form.validate()
            self.assertEqual('Invalid calculation_type: subtraction', str(ite.exception))

    def test_bespoke_message_for_sum_validation(self):
        store = AnswerStore()

        answer_total = Answer(
            answer_id='total-answer',
            answer_instance=1,
            group_instance=1,
            value=10,
        )

        store.add(answer_total)

        with self.test_request_context():
            schema = load_schema_from_params('test', 'sum_equal_validation_against_total')

            block_json = schema.get_block('breakdown-block')

            question_json = {
                'id': 'breakdown-question',
                'type': 'Calculated',
                'validation': {
                    'messages': {
                        'TOTAL_SUM_NOT_EQUALS': 'Test Message'
                    }
                },
                'calculations': [{
                    'calculation_type': 'sum',
                    'answer_id': 'total-answer',
                    'answers_to_calculate': [
                        'breakdown-1',
                        'breakdown-2'
                    ],
                    'conditions': [
                        'equals'
                    ]
                }],
                'answers': [{
                    'id': 'breakdown-1',
                    'label': 'Breakdown 1',
                    'type': 'Number'
                }, {
                    'id': 'breakdown-2',
                    'label': 'Breakdown 2',
                    'type': 'Number'
                }]
            }

            data = {
                'breakdown-1': '3',
                'breakdown-2': '5',
            }

            form = generate_form(schema, block_json, data, store, metadata=None)

            with patch('app.questionnaire.questionnaire_schema.QuestionnaireSchema.get_questions_for_block',
                       return_value=[question_json]):
                form.validate()
                self.assertIn(form.question_errors['breakdown-question'], 'Test Message')

    def test_empty_calculated_field(self):
        store = AnswerStore()

        answer_total = Answer(
            answer_id='total-answer',
            answer_instance=1,
            group_instance=1,
            value=10,
        )

        store.add(answer_total)

        with self.test_request_context():
            schema = load_schema_from_params('test', 'sum_equal_validation_against_total')

            block_json = schema.get_block('breakdown-block')

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
            form = generate_form(schema, block_json, data, store, metadata=None)

            form.validate()
            self.assertEqual(form.data, expected_form_data)
            self.assertEqual(form.question_errors['breakdown-question'], schema.error_messages['TOTAL_SUM_NOT_EQUALS']
                             % dict(total='10'), AnswerStore())

    def test_sum_calculated_field(self):
        store = AnswerStore()

        answer_total = Answer(
            answer_id='total-answer',
            answer_instance=1,
            group_instance=1,
            value=10,
        )

        store.add(answer_total)

        with self.test_request_context():
            schema = load_schema_from_params('test', 'sum_equal_validation_against_total')

            block_json = schema.get_block('breakdown-block')

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
            form = generate_form(schema, block_json, data, store, metadata=None)

            form.validate()
            self.assertEqual(form.data, expected_form_data)

    def test_get_calculation_total_with_no_input(self):
        store = AnswerStore()

        answer_total = Answer(
            answer_id='total-answer',
            answer_instance=1,
            group_instance=1,
            value=10,
        )

        store.add(answer_total)

        with self.test_request_context():
            schema = load_schema_from_params('test', 'sum_equal_validation_against_total')

            block_json = schema.get_block('breakdown-block')

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
            form = generate_form(schema, block_json, data, store, metadata=None)

            form.validate()
            self.assertEqual(form.data, expected_form_data)
            self.assertEqual(form.question_errors['breakdown-question'], schema.error_messages['TOTAL_SUM_NOT_EQUALS']
                             % dict(total='10'), AnswerStore())

    def test_multi_calculation(self):
        store = AnswerStore()

        answer_total = Answer(
            answer_id='total-answer',
            answer_instance=1,
            group_instance=1,
            value=10,
        )

        store.add(answer_total)

        with self.test_request_context():
            schema = load_schema_from_params('test', 'sum_multi_validation_against_total')

            block_json = schema.get_block('breakdown-block')

            data = {
                'breakdown-1': '',
                'breakdown-2': '',
                'breakdown-3': '',
                'breakdown-4': ''
            }

            # With no answers question validation should pass
            form = generate_form(schema, block_json, data, store, metadata=None)
            form.validate()

            self.assertEqual(len(form.question_errors), 0)

            # With the data equaling the total question validation should pass
            data['breakdown-1'] = '10'

            form = generate_form(schema, block_json, data, store, metadata=None)
            form.validate()

            self.assertEqual(len(form.question_errors), 0)

            # With the data not equaling zero or the total, question validation should fail
            data['breakdown-1'] = '1'

            form = generate_form(schema, block_json, data, store, metadata=None)
            form.validate()

            self.assertEqual(form.question_errors['breakdown-question'],
                             schema.error_messages['TOTAL_SUM_NOT_EQUALS'] % dict(total='10'))

    def test_form_errors_are_correctly_mapped(self):
        with self.test_request_context():
            schema = load_schema_from_params('test', '0112')

            block_json = schema.get_block('total-retail-turnover')

            form = generate_form(schema, block_json, {}, AnswerStore(), metadata=None)

            form.validate()
            mapped_errors = form.map_errors()

            self.assertTrue(self._error_exists('total-retail-turnover-answer', schema.error_messages
                                               ['MANDATORY_NUMBER'], mapped_errors))

    def test_form_subfield_errors_are_correctly_mapped(self):
        with self.test_request_context():
            schema = load_schema_from_params('test', '0102')

            block_json = schema.get_block('reporting-period')

            form = generate_form(schema, block_json, {}, AnswerStore(), metadata=None)

            form.validate()
            mapped_errors = form.map_errors()

            self.assertTrue(self._error_exists('period-to', schema.error_messages['MANDATORY_DATE'], mapped_errors))
            self.assertTrue(self._error_exists('period-from', schema.error_messages['MANDATORY_DATE'], mapped_errors))

    def test_answer_with_child_inherits_mandatory_from_parent(self):
        with self.test_request_context():
            schema = load_schema_from_params('test', 'radio_mandatory_with_mandatory_other')

            block_json = schema.get_block('radio-mandatory')

            form = generate_form(schema, block_json, {
                'radio-mandatory-answer': 'Other'
            }, AnswerStore(), metadata=None)

            child_field = getattr(form, 'other-answer-mandatory')

            self.assertIsInstance(child_field.validators[0], ResponseRequired)

    def test_answer_with_child_errors_are_correctly_mapped(self):
        with self.test_request_context():
            schema = load_schema_from_params('test', 'radio_mandatory_with_mandatory_other')

            block_json = schema.get_block('radio-mandatory')

            form = generate_form(schema, block_json, {
                'radio-mandatory-answer': 'Other'
            }, AnswerStore(), metadata=None)

            form.validate()
            mapped_errors = form.map_errors()

            self.assertTrue(self._error_exists('radio-mandatory-answer', schema.error_messages['MANDATORY_TEXTFIELD'],
                                               mapped_errors))
            self.assertFalse(self._error_exists('other-answer-mandatory', schema.error_messages['MANDATORY_TEXTFIELD'],
                                                mapped_errors))

    def test_answer_errors_are_interpolated(self):
        with self.test_request_context():
            schema = load_schema_from_params('test', '0112')

            block_json = schema.get_block('number-of-employees')

            form = generate_form(schema, block_json, {
                'total-number-employees': '-1'
            }, AnswerStore(), metadata=None)

            form.validate()
            answer_errors = form.answer_errors('total-number-employees')
            self.assertIn(schema.error_messages['NUMBER_TOO_SMALL'] % dict(min='0'), answer_errors)

    def test_option_has_other(self):
        with self.test_request_context():
            schema = load_schema_from_params('test', 'checkbox')
            block_json = schema.get_block('mandatory-checkbox')

            form = generate_form(schema, block_json, {}, AnswerStore(), metadata=None)

            self.assertFalse(form.option_has_other('mandatory-checkbox-answer', 1))
            self.assertTrue(form.option_has_other('mandatory-checkbox-answer', 6))

    def test_get_other_answer(self):
        with self.test_request_context():
            schema = load_schema_from_params('test', 'checkbox')
            block_json = schema.get_block('mandatory-checkbox')

            form = generate_form(schema, block_json, {
                'other-answer-mandatory': 'Some data'
            }, AnswerStore(), metadata=None)

            field = form.get_other_answer('mandatory-checkbox-answer', 6)

            self.assertEqual('Some data', field.data)

    def test_get_other_answer_invalid(self):
        with self.test_request_context():
            schema = load_schema_from_params('test', 'checkbox')
            block_json = schema.get_block('mandatory-checkbox')

            form = generate_form(schema, block_json, {
                'other-answer-mandatory': 'Some data'
            }, AnswerStore(), metadata=None)

            field = form.get_other_answer('mandatory-checkbox-answer', 4)

            self.assertEqual(None, field)
