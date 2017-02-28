from app.questionnaire.rules import evaluate_rule
from app.helpers.schema_helper import SchemaHelper

from tests.app.framework.survey_runner_test_case import SurveyRunnerTestCase


class TestConditionalDisplay(SurveyRunnerTestCase):

    def setUp(self):
        super().setUp()
        self.question_map = SchemaHelper.get_questions_by_id(self.schema_json)

    def tearDown(self):
        super().tearDown()

    def test_skip_condition_false(self):
        answer = "Bothans"
        # find the question with the 'not equals' skip condition
        question = self.question_map["rebel-alliance-question"]

        # check the skip condition exists
        self.assertIsNotNone(question['skip_condition'])

        # the condition will fire now as we have answer the question correctly, so we won't skip the question
        self.assertFalse(evaluate_rule(question['skip_condition']['when'][0], answer))

    def test_skip_condition_true(self):
        answer = "Some other answer"

        # find the question with the 'not equals' skip condition
        question = self.question_map["rebel-alliance-question"]

        # check the skip condition exists
        self.assertIsNotNone(question['skip_condition'])

        # the condition won't fire as we haven't answered any questions, so we will skip the question
        self.assertTrue(evaluate_rule(question['skip_condition']['when'][0], answer))

    def test_skip_condition_blank(self):
        answer = ""

        # find the question with the 'not equals' skip condition
        question = self.question_map["rebel-alliance-question"]

        # check the skip condition exists
        self.assertIsNotNone(question['skip_condition'])

        # the condition won't fire as we haven't answered any questions, so we will skip the question
        self.assertTrue(evaluate_rule(question['skip_condition']['when'][0], answer))
