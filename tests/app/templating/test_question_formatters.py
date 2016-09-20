from app.templating.summary.summary_item import SummaryItem
from app.schema.question import Question
from app.schema.answer import Answer
from app.schema.block import Block
from app.schema.section import Section
from app.questionnaire_state.answer import Answer as StateAnswer
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

    def test_general_integer_missing_answer(self):

        original_answer = ''
        expected_format = None
        question_type = 'GENERAL'
        answer_type = 'INTEGER'
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

        block = Block()
        block.id = 'b1'
        section = Section()
        section.id = 's1'
        section.container = block
        question = Question()
        question.type = question_type
        question.id = 'q1'
        question.container = section
        answer = Answer()
        answer.type = answer_type
        answer.id = 'a1'
        answer.label = 'label'

        if answer_type == 'CHECKBOX' or answer_type == 'RADIO':
            answer.options = [{
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

        question.answers = [answer]
        state_answer = StateAnswer(question.id, question)
        state_answer.value = original_answer
        state_answers = [state_answer]
        section.questions = [question]

        summary_item = SummaryItem(question, state_answers, question.type)
        self.assertEqual(summary_item.answer, expected_format)
        self.assertEqual(summary_item.link, block.id + "#" + answer.id)
