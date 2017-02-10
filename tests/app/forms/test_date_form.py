import unittest

from app import create_app
from app.forms.date_form import get_date_form, get_month_year_form
from app.schema_loader.schema_loader import load_schema_file
from app.helpers.schema_helper import SchemaHelper


class TestDateForm(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['SERVER_NAME'] = "test"
        self.app_context = self.app.app_context()
        self.app_context.push()

    def test_generate_date_form_creates_empty_form(self):
        survey = load_schema_file("test_dates.json")
        block_json = SchemaHelper.get_block(survey, 'date-block')
        error_messages = SchemaHelper.get_messages(survey)

        answers = SchemaHelper.get_answers_by_id_for_block(block_json)

        form = get_date_form(answers['single-date-answer'], error_messages=error_messages)

        self.assertTrue(hasattr(form, 'day'))
        self.assertTrue(hasattr(form, 'month'))
        self.assertTrue(hasattr(form, 'year'))

    def test_generate_month_year_date_form_creates_empty_form(self):
        survey = load_schema_file("test_dates.json")
        block_json = SchemaHelper.get_block(survey, 'date-block')
        error_messages = SchemaHelper.get_messages(survey)

        answers = SchemaHelper.get_answers_by_id_for_block(block_json)

        form = get_month_year_form(answers['month-year-answer'], error_messages=error_messages)

        self.assertFalse(hasattr(form, 'day'))
        self.assertTrue(hasattr(form, 'month'))
        self.assertTrue(hasattr(form, 'year'))
