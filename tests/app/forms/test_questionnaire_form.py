from app.forms.questionnaire_form import generate_form
from app.utilities.schema import load_schema_from_params
from app.validation.validators import ResponseRequired
from app.data_model.answer_store import AnswerStore

from tests.app.app_context_test_case import AppContextTestCase


class TestQuestionnaireForm(AppContextTestCase):

    @staticmethod
    def _error_exists(answer_id, msg, mapped_errors):
        return any(a_id == answer_id and msg in ordered_errors for a_id, ordered_errors in mapped_errors)

    def test_form_ids_match_block_answer_ids(self):
        with self.test_request_context():
            schema = load_schema_from_params('test', '0102')

            block_json = schema.get_block('reporting-period')

            form = generate_form(schema, block_json, {}, AnswerStore())

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
            form = generate_form(schema, block_json, data, AnswerStore())

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
            form = generate_form(schema, block_json, data, AnswerStore())

            form.validate()
            self.assertEqual(form.data, expected_form_data)
            self.assertEqual(form.question_errors['reporting-period-question'], schema.error_messages['INVALID_DATE_RANGE'])

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
            form = generate_form(schema, block_json, data, AnswerStore())

            form.validate()
            self.assertEqual(form.data, expected_form_data)
            self.assertEqual(form.question_errors['reporting-period-question'], schema.error_messages['INVALID_DATE_RANGE'], AnswerStore())

    def test_form_errors_are_correctly_mapped(self):
        with self.test_request_context():
            schema = load_schema_from_params('test', '0112')

            block_json = schema.get_block('total-retail-turnover')

            form = generate_form(schema, block_json, {}, AnswerStore())

            form.validate()
            mapped_errors = form.map_errors()

            self.assertTrue(self._error_exists('total-retail-turnover-answer', schema.error_messages['MANDATORY_NUMBER'], mapped_errors))

    def test_form_subfield_errors_are_correctly_mapped(self):
        with self.test_request_context():
            schema = load_schema_from_params('test', '0102')

            block_json = schema.get_block('reporting-period')

            form = generate_form(schema, block_json, {}, AnswerStore())

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
            }, AnswerStore())

            child_field = getattr(form, 'other-answer-mandatory')

            self.assertIsInstance(child_field.validators[0], ResponseRequired)

    def test_answer_with_child_errors_are_correctly_mapped(self):
        with self.test_request_context():
            schema = load_schema_from_params('test', 'radio_mandatory_with_mandatory_other')

            block_json = schema.get_block('radio-mandatory')

            form = generate_form(schema, block_json, {
                'radio-mandatory-answer': 'Other'
            }, AnswerStore())

            form.validate()
            mapped_errors = form.map_errors()

            self.assertTrue(self._error_exists('radio-mandatory-answer', schema.error_messages['MANDATORY_TEXTFIELD'], mapped_errors))
            self.assertFalse(self._error_exists('other-answer-mandatory', schema.error_messages['MANDATORY_TEXTFIELD'], mapped_errors))

    def test_answer_errors_are_interpolated(self):
        with self.test_request_context():
            schema = load_schema_from_params('test', '0112')

            block_json = schema.get_block('number-of-employees')

            form = generate_form(schema, block_json, {
                'total-number-employees': '-1'
            }, AnswerStore())

            form.validate()
            answer_errors = form.answer_errors('total-number-employees')
            self.assertIn(schema.error_messages['NUMBER_TOO_SMALL'] % dict(min='0'), answer_errors)

    def test_option_has_other(self):
        with self.test_request_context():
            schema = load_schema_from_params('test', 'checkbox')
            block_json = schema.get_block('mandatory-checkbox')

            form = generate_form(schema, block_json, {}, AnswerStore())

            self.assertFalse(form.option_has_other('mandatory-checkbox-answer', 1))
            self.assertTrue(form.option_has_other('mandatory-checkbox-answer', 6))

    def test_get_other_answer(self):
        with self.test_request_context():
            schema = load_schema_from_params('test', 'checkbox')
            block_json = schema.get_block('mandatory-checkbox')

            form = generate_form(schema, block_json, {
                'other-answer-mandatory': 'Some data'
            }, AnswerStore())

            field = form.get_other_answer('mandatory-checkbox-answer', 6)

            self.assertEqual('Some data', field.data)

    def test_get_other_answer_invalid(self):
        with self.test_request_context():
            schema = load_schema_from_params('test', 'checkbox')
            block_json = schema.get_block('mandatory-checkbox')

            form = generate_form(schema, block_json, {
                'other-answer-mandatory': 'Some data'
            }, AnswerStore())

            field = form.get_other_answer('mandatory-checkbox-answer', 4)

            self.assertEqual(None, field)
