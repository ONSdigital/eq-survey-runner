
from app.questionnaire.questionnaire_manager_factory import QuestionnaireManagerFactory
from app.questionnaire_state.node import Node
from app.questionnaire.user_journey import UserJourney
from app.questionnaire.user_journey_manager import UserJourneyManager
from tests.app.framework.sr_unittest import SurveyRunnerTestCase

from unittest.mock import MagicMock


class TestQuestionnaireManagerFactory(SurveyRunnerTestCase):

    def setUp(self):
        super().setUp()
        self.has_user_journey = UserJourneyManager.has_user_journey
        self.get_user_journey = UserJourneyManager.get_user_journey
        self.get_schema = QuestionnaireManagerFactory._get_schema
        QuestionnaireManagerFactory._get_schema = lambda: self.questionnaire

    def tearDown(self):
        super().tearDown()
        UserJourneyManager.has_user_journey = self.has_user_journey
        UserJourneyManager.get_user_journey = self.get_user_journey
        QuestionnaireManagerFactory._get_schema = self.get_schema

    def test_get_instance(self):
        with self.application.test_request_context():
            self.assertIsNotNone(QuestionnaireManagerFactory.get_instance())

    def mock_user_journey(self):
        UserJourneyManager.has_user_journey = MagicMock(return_value="True")
        node = Node("1", None)
        user_journey = UserJourney(self.questionnaire, current_node=node, first_node=node, tail_node=node, valid_locations=[],
                            archive={}, submitted_at=None)
        return user_journey
