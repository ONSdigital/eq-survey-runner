from unittest import mock

from mock import Mock, MagicMock

from app.templating.summary.summary_item import SummaryItem
from tests.app.framework.sr_unittest import SurveyRunnerTestCase


class TestQuestionFormatters(SurveyRunnerTestCase):

    def test_general_currency(self):

        original_answer = 1000
        expected_format = '£1,000'
        question_type = 'GENERAL'
        answer_type = 'CURRENCY'
        self.check_formatter(answer_type, question_type, expected_format, original_answer)

    def test_general_text_area(self):

        original_answer = 'text area test'
        expected_format = 'text area test'
        question_type = 'GENERAL'
        answer_type = 'TEXTAREA'
        self.check_formatter(answer_type, question_type, expected_format, original_answer)

    def test_general_radio(self):

        original_answer = 'value_test_1'
        expected_format = 'label_test_1'
        question_type = 'GENERAL'
        answer_type = 'RADIO'
        self.check_formatter(answer_type, question_type, expected_format, original_answer)

    def test_general_checkbox(self):

        original_answer = ['value_test_1','value_test_2']
        expected_format = ['label_test_1', 'label_test_2']
        question_type = 'GENERAL'
        answer_type = 'CHECKBOX'
        self.check_formatter(answer_type, question_type, expected_format, original_answer)

    def test_general_text_field(self):

        original_answer = 'text field test'
        expected_format = 'text field test'
        question_type = 'GENERAL'
        answer_type = 'TEXTFIELD'
        self.check_formatter(answer_type, question_type, expected_format, original_answer)

    def test_general_positive_integer(self):

        original_answer = '12345'
        expected_format = '12345'
        question_type = 'GENERAL'
        answer_type = 'POSITIVEINTEGER'
        self.check_formatter(answer_type, question_type, expected_format, original_answer)

    def test_general_positive_integer_zero(self):

        original_answer = 0
        expected_format = 0
        question_type = 'GENERAL'
        answer_type = 'POSITIVEINTEGER'
        self.check_formatter(answer_type, question_type, expected_format, original_answer)

    def test_general_integer(self):

        original_answer = '12345'
        expected_format = '12345'
        question_type = 'GENERAL'
        answer_type = 'INTEGER'
        self.check_formatter(answer_type, question_type, expected_format, original_answer)

    def check_formatter(self, answer_type, question_type, expected_format, original_answer):
        answer = Mock()
        answer.value = original_answer
        answer.id = 'answerid'
        answers = Mock()
        answers.__iter__ = Mock(return_value=iter([answer]))
        answer_schema = Mock()
        answer_schema.type.lower = Mock(return_value=answer_type)
        question_schema = MagicMock()
        question_schema.questionnaire.get_item_by_id = Mock(return_value=answer_schema)
        question_schema.container.container.id = 'blockid'

        if answer_type == 'CHECKBOX' or answer_type == 'RADIO':
            question_schema.answers[0].options = [{
                              "label": "label_test_1",
                              "value": "value_test_1"
                              },
                              {
                              "label": "label_test_2",
                              "value": "value_test_2"
                              },
                              {
                              "label": "label_test_3",
                              "value": "value_test_3"
                              }]

        summary_item = SummaryItem(question_schema, answers, question_type)
        self.assertEqual(summary_item.sub_items[0].answer, expected_format)
        self.assertEqual(summary_item.sub_items[0].link, 'blockid#answerid')
