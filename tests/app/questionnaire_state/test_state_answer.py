import unittest

from werkzeug.datastructures import MultiDict

from app.questionnaire_state.state_answer import StateAnswer
from app.schema.answer import Answer
from app.schema.widgets.text_widget import TextWidget


class TestStateAnswer(unittest.TestCase):

    def setUp(self):
        self.answer_schema = Answer('multiple-choice-with-other')
        self.answer_schema.widget = TextWidget(self.answer_schema.id)
        self.answer_schema.options = [
            {
                "label": "Yes",
                "value": "Yes"
            },
            {
                "label": "No",
                "value": "No",
                "other": {
                    "label": "Please enter the country of usual residence"
                }
            }
        ]

    def test_should_restore_other_value(self):
        # Given
        answer = StateAnswer(self.answer_schema.id, self.answer_schema)
        answer.input = 'Some entered value'

        post_vars = {
            'multiple-choice-with-other': 'Some entered value',
        }

        # When
        answer._restore_other_value(post_vars)

        # Then
        self.assertEqual(answer.other, 'Some entered value')

    def test_should_set_input_to_schema_option_label_value(self):
        # Given
        answer = StateAnswer(self.answer_schema.id, self.answer_schema)
        answer.input = 'Some entered value'

        post_vars = {
            'multiple-choice-with-other': 'Some entered value',
        }

        # When
        answer._restore_other_value(post_vars)

        # Then
        self.assertEqual(answer.input, 'No')

    def test_should_select_schema_option_if_other_input_text_already_an_option_in_the_schema(self):
        # Given
        answer = StateAnswer(self.answer_schema.id, self.answer_schema)
        answer.input = 'No'

        post_vars = MultiDict()
        post_vars.add('multiple-choice-with-other', 'No')
        post_vars.add('multiple-choice-with-other', 'Yes')

        # When
        answer._restore_other_value(post_vars)

        # Then
        self.assertEqual(answer.input, 'Yes')

    def test_should_deselect_other_if_other_input_text_option_in_schema(self):
        # Given
        answer = StateAnswer(self.answer_schema.id, self.answer_schema)
        answer.input = 'No'

        post_vars = MultiDict()
        post_vars.add('multiple-choice-with-other', 'No')
        post_vars.add('multiple-choice-with-other', 'Yes')

        # When
        answer._restore_other_value(post_vars)

        # Then
        self.assertIsNone(answer.other)


