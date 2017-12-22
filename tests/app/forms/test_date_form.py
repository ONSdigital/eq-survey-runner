from app.forms.date_form import get_date_form, get_month_year_form
from app.utilities.schema import load_schema_from_params
from tests.app.app_context_test_case import AppContextTestCase


class TestDateForm(AppContextTestCase):

    def test_generate_date_form_creates_empty_form(self):
        schema = load_schema_from_params('test', 'dates')
        error_messages = schema.error_messages

        answers = schema.get_answers_by_id_for_block('date-block')

        form = get_date_form(answers['single-date-answer'], error_messages=error_messages)

        self.assertTrue(hasattr(form, 'day'))
        self.assertTrue(hasattr(form, 'month'))
        self.assertTrue(hasattr(form, 'year'))

    def test_generate_month_year_date_form_creates_empty_form(self):
        schema = load_schema_from_params('test', 'dates')
        error_messages = schema.error_messages

        answers = schema.get_answers_by_id_for_block('date-block')

        form = get_month_year_form(answers['month-year-answer'], error_messages=error_messages)

        self.assertFalse(hasattr(form, 'day'))
        self.assertTrue(hasattr(form, 'month'))
        self.assertTrue(hasattr(form, 'year'))
