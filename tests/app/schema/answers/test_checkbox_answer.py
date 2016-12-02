from unittest import TestCase

from app.schema.answers.checkbox_answer import CheckboxAnswer
from app.schema.question import Question
from app.questionnaire_state.state_answer import StateAnswer
from app.questionnaire_state.state_question import StateQuestion
from unittest.mock import MagicMock


class TestCheckBoxAnswer(TestCase):

    def setUp(self):

        question = Question()
        question.skipped = False
        question.type = "General"
        question_state = StateQuestion('2', question)

        self.check_box_answer = CheckboxAnswer('1234')
        self.check_box_answer.type = "Checkbox"
        self.check_box_answer.mandatory = True
        self.check_box_answer.questionnaire = MagicMock()

        self.answer_state = StateAnswer('1', self.check_box_answer)
        self.answer_state.is_valid = True
        self.answer_state.parent = question_state
        self.answer_state.schema_item.options = [{"label": "Option1", "value": "Option1"},{"label": "Option2", "value": "Option2"}]

    def test_mandatory_check_box_answer_other_with_valid_other(self):
        self.answer_state.input = ['other', 'Option3']
        is_valid = self.check_box_answer.validate(self.answer_state)
        self.assertEquals(is_valid, True)

    def test_mandatory_check_box_answer_other_with_no_valid_other(self):
        self.answer_state.input = ['other']
        is_valid = self.check_box_answer.validate(self.answer_state)
        self.assertEquals(is_valid, False)
        self.check_box_answer.questionnaire.get_error_message.assert_called_with('MANDATORY', '1234')

    def test_mandatory_check_box_answer_without_other_identifier(self):
        self.answer_state.input = ['Option3']
        is_valid = self.check_box_answer.validate(self.answer_state)
        self.assertEquals(is_valid, False)
        self.check_box_answer.questionnaire.get_error_message.assert_called_with('MANDATORY', '1234')

    def test_mandatory_check_box_answer_without_input(self):
        self.answer_state.input = None
        is_valid = self.check_box_answer.validate(self.answer_state)
        self.assertEquals(is_valid, False)
        self.check_box_answer.questionnaire.get_error_message.assert_called_with('MANDATORY', '1234')

    def test_non_mandatory_check_box_answer_empty(self):
        self.answer_state.input = None
        self.answer_state.is_valid = True
        self.check_box_answer.mandatory = False
        is_valid = self.check_box_answer.validate(self.answer_state)
        self.assertEquals(is_valid, True)

    def test_non_mandatory_check_box_answer_non_valid_other_value(self):
        self.answer_state.input = ['other'] # other doesn't need an associated value if non_mandatory
        self.answer_state.is_valid = True
        self.check_box_answer.mandatory = False
        is_valid = self.check_box_answer.validate(self.answer_state)
        self.assertEquals(is_valid, True)

    def test_check_box_answer_skipped(self):
        self.answer_state.is_valid = True
        self.answer_state.parent.skipped = True
        is_valid = self.check_box_answer.validate(self.answer_state)
        self.assertEquals(is_valid, True)
