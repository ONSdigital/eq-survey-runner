import unittest

from wtforms import validators

from app import create_app
from app.forms.questionnaire_form import generate_form
from app.helpers.schema_helper import SchemaHelper
from app.schema_loader.schema_loader import load_schema_file


class TestQuestionnaireForm(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['SERVER_NAME'] = "test"
        self.app_context = self.app.app_context()
        self.app_context.push()

    @staticmethod
    def _error_exists(answer_id, msg, mapped_errors):
        return any(a_id == answer_id and msg in ordered_errors for a_id, ordered_errors in mapped_errors)

    def test_form_ids_match_block_answer_ids(self):
        survey = load_schema_file("1_0102.json")

        block_json = SchemaHelper.get_block(survey, "reporting-period")
        error_messages = SchemaHelper.get_messages(survey)

        form = generate_form(block_json, {}, error_messages)

        for answer in SchemaHelper.get_answers_for_block(block_json):
            self.assertTrue(hasattr(form, answer['id']))

    def test_form_date_range_populates_data(self):
        survey = load_schema_file("1_0102.json")

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
            'period-from': {'day': '01', 'month': '3', 'year': '2016'},
            'period-to': {'day': '31', 'month': '3', 'year': '2016'}
        }
        form = generate_form(block_json, data, error_messages)

        self.assertEqual(form.data, expected_form_data)

    def test_date_range_matching_dates_raises_question_error(self):
        survey = load_schema_file("1_0102.json")

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
            'period-from': {'day': '25', 'month': '12', 'year': '2016'},
            'period-to': {'day': '25', 'month': '12', 'year': '2016'}
        }
        form = generate_form(block_json, data, error_messages)

        expected_message = "The 'period to' date must be different to the 'period from' date."

        form.validate()
        self.assertEqual(form.data, expected_form_data)
        self.assertEqual(form.question_errors['reporting-period-question'], expected_message)

    def test_date_range_to_precedes_from_raises_question_error(self):
        survey = load_schema_file("1_0102.json")

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
            'period-from': {'day': '25', 'month': '12', 'year': '2016'},
            'period-to': {'day': '24', 'month': '12', 'year': '2016'}
        }
        form = generate_form(block_json, data, error_messages)

        expected_message = "The 'period to' date cannot be before the 'period from' date."

        form.validate()
        self.assertEqual(form.data, expected_form_data)
        self.assertEqual(form.question_errors['reporting-period-question'], expected_message)

    def test_form_errors_are_correctly_mapped(self):
        survey = load_schema_file("1_0112.json")

        block_json = SchemaHelper.get_block(survey, "total-retail-turnover")
        error_messages = SchemaHelper.get_messages(survey)

        form = generate_form(block_json, {}, error_messages)

        form.validate()
        mapped_errors = form.map_errors()

        message = "Please provide a value, even if your value is 0."

        self.assertTrue(self._error_exists('total-retail-turnover-answer', message, mapped_errors))

    def test_form_subfield_errors_are_correctly_mapped(self):
        survey = load_schema_file("1_0102.json")

        block_json = SchemaHelper.get_block(survey, "reporting-period")
        error_messages = SchemaHelper.get_messages(survey)

        form = generate_form(block_json, {}, error_messages)

        message = "Please provide an answer to continue."

        form.validate()
        mapped_errors = form.map_errors()

        self.assertTrue(self._error_exists('period-to', message, mapped_errors))
        self.assertTrue(self._error_exists('period-from', message, mapped_errors))

    def test_answer_with_child_inherits_mandatory_from_parent(self):
        survey = load_schema_file("test_radio.json")

        block_json = SchemaHelper.get_block(survey, "block-1")
        error_messages = SchemaHelper.get_messages(survey)

        form = generate_form(block_json, {
            'ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c': 'Other'
        }, error_messages)

        child_field = getattr(form, 'other-answer-mandatory')

        self.assertIsInstance(child_field.validators[0], validators.InputRequired)

    def test_answer_with_child_errors_are_correctly_mapped(self):
        survey = load_schema_file("test_radio.json")

        block_json = SchemaHelper.get_block(survey, "block-1")
        error_messages = SchemaHelper.get_messages(survey)

        form = generate_form(block_json, {
            'ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c': 'Other'
        }, error_messages)

        form.validate()
        mapped_errors = form.map_errors()

        message = "This field is mandatory."

        self.assertTrue(self._error_exists("ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c", message, mapped_errors))
        self.assertFalse(self._error_exists("other-answer-mandatory", message, mapped_errors))

    def test_answer_errors_are_mapped(self):
        survey = load_schema_file("1_0112.json")

        block_json = SchemaHelper.get_block(survey, "total-retail-turnover")
        error_messages = SchemaHelper.get_messages(survey)

        form = generate_form(block_json, {
            'total-retail-turnover-answer': "-1"
        }, error_messages)

        form.validate()
        answer_errors = form.answer_errors('total-retail-turnover-answer')
        self.assertIn("The value cannot be negative. Please correct your answer.", answer_errors)
