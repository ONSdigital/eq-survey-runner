from unittest import TestCase
from unittest.mock import Mock, MagicMock

from app.templating.summary.formatters.radio_button import RadioButtonFormatter


class TestRadioFormatter(TestCase):

    def setUp(self):
        self._other_option = {'value': 'other', 'label': 'Other'}
        self._user_answers = 'other'

    def test_other_selected_but_no_value_provided(self):
        schema_answers = MagicMock()
        schema_answers[0].options = [self._other_option]

        state_answers = MagicMock()
        state_answers[0].other = None

        answers = RadioButtonFormatter.format(schema_answers, state_answers, self._user_answers)
        self.assertIn('Other', answers)

    def test_other_selected_and_value_provided(self):
        schema_answers = MagicMock()
        schema_answers[0].options = [self._other_option]

        state_answers = MagicMock()
        state_answers[0].other = 'The entered value'

        answers = RadioButtonFormatter.format(schema_answers, state_answers, self._user_answers)
        self.assertIn('The entered value', answers)
