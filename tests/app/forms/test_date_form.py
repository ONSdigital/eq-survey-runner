import unittest

from app import create_app
from app.forms.date_form import get_date_form, get_month_year_form, get_date_data, get_date_range_fields
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

    def test_get_date_data(self):
        form_data = {
            'some-answer-id-day': '1',
            'some-answer-id-month': '01',
            'some-answer-id-year': '2016'
        }
        expected = {
            'day': '1',
            'month': '01',
            'year': '2016'
        }
        actual = get_date_data(form_data, "some-answer-id")

        self.assertEqual(actual, expected)

    def test_get_date_data_rejects_invalid(self):
        form_data = {
            'some-answer-id-day': '1',
            'some-answer-id-month': '01'
        }
        actual = get_date_data(form_data, "some-answer-id")

        self.assertEqual(actual, None)

    def test_get_date_range_fields(self):
        survey = load_schema_file("test_dates.json")
        error_messages = SchemaHelper.get_messages(survey)

        questions = SchemaHelper.get_questions_by_id(survey)

        from_field, to_field = get_date_range_fields(questions["date-range-question"], {
            'day': '1',
            'month': '01',
            'year': '2016'
        }, error_messages)

        self.assertTrue(hasattr(from_field.args[0], 'day'))
        self.assertTrue(hasattr(from_field.args[0], 'month'))
        self.assertTrue(hasattr(from_field.args[0], 'year'))

        self.assertTrue(hasattr(to_field.args[0], 'day'))
        self.assertTrue(hasattr(to_field.args[0], 'month'))
        self.assertTrue(hasattr(to_field.args[0], 'year'))
