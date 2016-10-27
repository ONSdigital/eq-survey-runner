from unittest import TestCase
from unittest.mock import Mock, MagicMock

from app.templating.summary.formatters.check_box import CheckBoxFormatter


class TestCheckBoxFormatter(TestCase):

    def test_formatter_outputs_other_if_other_selected_but_no_value_specified(self):

        other_option = {'value': 'other'}
        schema_answers = MagicMock()
        schema_answers[0].options = [other_option]

        state_answers = MagicMock()
        state_answers[0].other = None

        user_answers = ['other']

        answers = CheckBoxFormatter.format(schema_answers, state_answers, user_answers)
        self.assertIn('Other', answers)

    def test_formatter_outputs_other_value_when_provided(self):
        other_option = {'value': 'other'}
        schema_answers = MagicMock()
        schema_answers[0].options = [other_option]

        state_answers = MagicMock()
        state_answers[0].other = 'The entered value'

        user_answers = ['other']

        answers = CheckBoxFormatter.format(schema_answers, state_answers, user_answers)
        self.assertIn('The entered value', answers)
