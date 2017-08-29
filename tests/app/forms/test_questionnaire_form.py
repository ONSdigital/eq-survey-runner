from app.forms.questionnaire_form import generate_form
from app.helpers.schema_helper import SchemaHelper
from app.utilities.schema import load_schema_file
from app.validation.validators import ResponseRequired
from app.data_model.answer_store import AnswerStore

from tests.app.app_context_test_case import AppContextTestCase


class TestQuestionnaireForm(AppContextTestCase):

    @staticmethod
    def _error_exists(answer_id, msg, mapped_errors):
        return any(a_id == answer_id and msg in ordered_errors for a_id, ordered_errors in mapped_errors)

    def test_form_ids_match_block_answer_ids(self):
        with self.test_request_context():
            survey = load_schema_file("test_0102.json")

            block_json = SchemaHelper.get_block(survey, "reporting-period")
            error_messages = SchemaHelper.get_messages(survey)

            form = generate_form(block_json, {}, error_messages, AnswerStore())

            for answer in SchemaHelper.get_answers_for_block(block_json):
                self.assertTrue(hasattr(form, answer['id']))

    def test_form_date_range_populates_data(self):
        with self.test_request_context():
            survey = load_schema_file("test_0102.json")

            block_json = SchemaHelper.get_block(survey, "reporting-period")
            error_messages = SchemaHelper.get_messages(survey)

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
            form = generate_form(block_json, data, error_messages, AnswerStore())

            self.assertEqual(form.data, expected_form_data)

    def test_date_range_matching_dates_raises_question_error(self):
        with self.test_request_context():
            survey = load_schema_file("test_0102.json")

            block_json = SchemaHelper.get_block(survey, "reporting-period")
            error_messages = SchemaHelper.get_messages(survey)

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
            form = generate_form(block_json, data, error_messages, AnswerStore())

            form.validate()
            self.assertEqual(form.data, expected_form_data)
            self.assertEqual(form.question_errors['reporting-period-question'], error_messages["INVALID_DATE_RANGE"])

    def test_date_range_to_precedes_from_raises_question_error(self):
        with self.test_request_context():
            survey = load_schema_file("test_0102.json")

            block_json = SchemaHelper.get_block(survey, "reporting-period")
            error_messages = SchemaHelper.get_messages(survey)

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
            form = generate_form(block_json, data, error_messages, AnswerStore())

            form.validate()
            self.assertEqual(form.data, expected_form_data)
            self.assertEqual(form.question_errors['reporting-period-question'], error_messages['INVALID_DATE_RANGE'], AnswerStore())

    def test_form_errors_are_correctly_mapped(self):
        with self.test_request_context():
            survey = load_schema_file("test_0112.json")

            block_json = SchemaHelper.get_block(survey, "total-retail-turnover")
            error_messages = SchemaHelper.get_messages(survey)

            form = generate_form(block_json, {}, error_messages, AnswerStore())

            form.validate()
            mapped_errors = form.map_errors()

            self.assertTrue(self._error_exists('total-retail-turnover-answer', error_messages["MANDATORY_NUMBER"], mapped_errors))

    def test_form_subfield_errors_are_correctly_mapped(self):
        with self.test_request_context():
            survey = load_schema_file("test_0102.json")

            block_json = SchemaHelper.get_block(survey, "reporting-period")
            error_messages = SchemaHelper.get_messages(survey)

            form = generate_form(block_json, {}, error_messages, AnswerStore())

            form.validate()
            mapped_errors = form.map_errors()

            self.assertTrue(self._error_exists('period-to', error_messages["MANDATORY_DATE"], mapped_errors))
            self.assertTrue(self._error_exists('period-from', error_messages["MANDATORY_DATE"], mapped_errors))

    def test_answer_with_child_inherits_mandatory_from_parent(self):
        with self.test_request_context():
            survey = load_schema_file("test_radio.json")

            block_json = SchemaHelper.get_block(survey, "radio-mandatory")
            error_messages = SchemaHelper.get_messages(survey)

            form = generate_form(block_json, {
                'radio-mandatory-answer': 'Other'
            }, error_messages, AnswerStore())

            child_field = getattr(form, 'other-answer-mandatory')

            self.assertIsInstance(child_field.validators[0], ResponseRequired)

    def test_answer_with_child_errors_are_correctly_mapped(self):
        with self.test_request_context():
            survey = load_schema_file("test_radio.json")

            block_json = SchemaHelper.get_block(survey, 'radio-mandatory')
            error_messages = SchemaHelper.get_messages(survey)

            form = generate_form(block_json, {
                'radio-mandatory-answer': 'Other'
            }, error_messages, AnswerStore())

            form.validate()
            mapped_errors = form.map_errors()

            self.assertTrue(self._error_exists("radio-mandatory-answer", error_messages['MANDATORY_TEXTFIELD'], mapped_errors))
            self.assertFalse(self._error_exists("other-answer-mandatory", error_messages['MANDATORY_TEXTFIELD'], mapped_errors))

    def test_answer_errors_are_mapped(self):
        with self.test_request_context():
            survey = load_schema_file("test_0112.json")

            block_json = SchemaHelper.get_block(survey, "total-retail-turnover")
            error_messages = SchemaHelper.get_messages(survey)

            form = generate_form(block_json, {
                'total-retail-turnover-answer': "-1"
            }, error_messages, AnswerStore())

            form.validate()
            answer_errors = form.answer_errors('total-retail-turnover-answer')
            self.assertIn(error_messages["NUMBER_TOO_SMALL"] % dict(min=0), answer_errors)

    def test_option_has_other(self):
        with self.test_request_context():
            survey = load_schema_file("test_checkbox.json")
            block_json = SchemaHelper.get_block(survey, "mandatory-checkbox")
            error_messages = SchemaHelper.get_messages(survey)

            form = generate_form(block_json, {}, error_messages, AnswerStore())

            self.assertFalse(form.option_has_other("mandatory-checkbox-answer", 1))
            self.assertTrue(form.option_has_other("mandatory-checkbox-answer", 6))

    def test_get_other_answer(self):
        with self.test_request_context():
            survey = load_schema_file("test_checkbox.json")
            block_json = SchemaHelper.get_block(survey, "mandatory-checkbox")
            error_messages = SchemaHelper.get_messages(survey)

            form = generate_form(block_json, {
                "other-answer-mandatory": "Some data"
            }, error_messages, AnswerStore())

            field = form.get_other_answer("mandatory-checkbox-answer", 6)

            self.assertEqual("Some data", field.data)

    def test_get_other_answer_invalid(self):
        with self.test_request_context():
            survey = load_schema_file("test_checkbox.json")
            block_json = SchemaHelper.get_block(survey, "mandatory-checkbox")
            error_messages = SchemaHelper.get_messages(survey)

            form = generate_form(block_json, {
                "other-answer-mandatory": "Some data"
            }, error_messages, AnswerStore())

            field = form.get_other_answer("mandatory-checkbox-answer", 4)

            self.assertEqual(None, field)
