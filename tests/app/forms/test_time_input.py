import unittest

from app import create_app
from app.forms.time_input_form import get_time_input_form
from app.schema_loader.schema_loader import load_schema_file
from app.helpers.schema_helper import SchemaHelper


class TestTimeInputForm(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['SERVER_NAME'] = "test"
        self.app_context = self.app.app_context()
        self.app_context.push()

    def test_generate_time_input_mandatory_form(self):
        survey = load_schema_file("test_time_input.json")
        block_json = SchemaHelper.get_block(survey, 'time-input-block')
        error_messages = SchemaHelper.get_messages(survey)

        answers = SchemaHelper.get_answers_by_id_for_block(block_json)

        form = get_time_input_form(answers['time-input-mandatory-answer'], error_messages=error_messages)

        self.assertTrue(hasattr(form, 'hours'))
        self.assertTrue(hasattr(form, 'mins'))

    def test_generate_time_input_non_mandatory_form(self):
        survey = load_schema_file("test_time_input.json")
        block_json = SchemaHelper.get_block(survey, 'time-input-block')
        error_messages = None

        answers = SchemaHelper.get_answers_by_id_for_block(block_json)

        form = get_time_input_form(answers['time-input-non-mandatory-answer'], error_messages= error_messages)

        self.assertTrue(hasattr(form, 'hours'))
        self.assertTrue(hasattr(form, 'mins'))

