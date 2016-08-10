from app.routing.conditional_display import ConditionalDisplay

from app.questionnaire.questionnaire_manager import QuestionnaireManager

from tests.app.framework.sr_unittest import SurveyRunnerTestCase


class MockQuestionnaireManager(QuestionnaireManager):

    def find_answer(self, id):
        # always return the answer we're expecting for the test to pass
        return "Bothans"


class TestConditionalDisplay(SurveyRunnerTestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_skip_condition_false(self):
        # find the question with the skip condition
        question = self.questionnaire.get_item_by_id("048e40da-bca4-48e5-9885-0bb6413bef62")

        # check the parse has set up the skip condition
        self.assertIsNotNone(question.skip_condition)

        # the condition will fire now as we have answer the question correctly, so we won't skip the question
        self.assertFalse(ConditionalDisplay.is_skipped(item=question, questionnaire_manager=MockQuestionnaireManager(self.questionnaire)))

    def test_skip_condition_true(self):

        # find the question with the skip condition
        question = self.questionnaire.get_item_by_id("048e40da-bca4-48e5-9885-0bb6413bef62")

        # check the parse has set up the skip condition
        self.assertIsNotNone(question.skip_condition)

        # the condition won't fire as we haven't answered any questions, so we will skip the question
        self.assertTrue(ConditionalDisplay.is_skipped(item=question, questionnaire_manager=QuestionnaireManager(self.questionnaire)))
