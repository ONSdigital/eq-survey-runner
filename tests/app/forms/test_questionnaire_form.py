import unittest

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

    def test_form_ids_match_block_answer_ids(self):
        survey = load_schema_file("1_0102.json")

        block_json = SchemaHelper.get_block(survey, "reporting-period")
        error_messages = SchemaHelper.get_messages(survey)

        form = generate_form(block_json, {}, error_messages)

        for answer in SchemaHelper.get_answers_for_block(block_json):
            self.assertTrue(hasattr(form, answer['id']))

    def test_form_date_range_popluates_data(self):
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
