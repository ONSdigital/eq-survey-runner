from app.questionnaire.rules import evaluate_rule

from tests.app.framework.sr_unittest import SurveyRunnerTestCase


class TestConditionalDisplay(SurveyRunnerTestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_skip_condition_false(self):
        answer = "Bothans"
        # find the question with the 'not equals' skip condition
        question = self.questionnaire.get_item_by_id("048e40da-bca4-48e5-9885-0bb6413bef62")

        # check the parse has set up the skip condition
        self.assertIsNotNone(question.skip_condition.as_dict())

        # the condition will fire now as we have answer the question correctly, so we won't skip the question
        self.assertFalse(evaluate_rule(question.skip_condition.as_dict()['when'], answer))

    def test_skip_condition_true(self):
        answer = "Some other answer"

        # find the question with the 'not equals' skip condition
        question = self.questionnaire.get_item_by_id("048e40da-bca4-48e5-9885-0bb6413bef62")

        # check the parse has set up the skip condition
        self.assertIsNotNone(question.skip_condition.as_dict())

        # the condition won't fire as we haven't answered any questions, so we will skip the question
        self.assertTrue(evaluate_rule(question.skip_condition.as_dict()['when'], answer))

    def test_skip_condition_blank(self):
        answer = ""

        # find the question with the 'not equals' skip condition
        question = self.questionnaire.get_item_by_id("048e40da-bca4-48e5-9885-0bb6413bef62")

        # check the parse has set up the skip condition
        self.assertIsNotNone(question.skip_condition)

        # the condition won't fire as we haven't answered any questions, so we will skip the question
        self.assertTrue(evaluate_rule(question.skip_condition.as_dict()['when'], answer))
