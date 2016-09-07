import logging

from app.questionnaire.questionnaire_manager_factory import QuestionnaireManagerFactory
from app.questionnaire_state.node import Node
from app.questionnaire.state import State
from app.questionnaire.state_recovery import StateRecovery
from app.questionnaire.state_manager import StateManager
from tests.app.framework.sr_unittest import SurveyRunnerTestCase

from unittest.mock import MagicMock


class TestQuestionnaireManagerFactory(SurveyRunnerTestCase):

    def setUp(self):
        super().setUp()
        self.has_state = StateManager.has_state
        self.get_state = StateManager.get_state
        self.recover_from_post_data = StateRecovery.recover_from_post_data
        self.get_schema = QuestionnaireManagerFactory._get_schema
        QuestionnaireManagerFactory._get_schema = lambda: self.questionnaire

    def tearDown(self):
        super().tearDown()
        StateManager.has_state = self.has_state
        StateManager.get_state = self.get_state
        StateRecovery.recover_from_post_data = self.recover_from_post_data
        QuestionnaireManagerFactory._get_schema = self.get_schema

    def test_get_instance(self):
        with self.application.test_request_context():
            self.assertIsNotNone(QuestionnaireManagerFactory.get_instance())

    def test_get_instance_git_revision_change(self):
        with self.application.test_request_context():
            state = self.mock_state()
            state.revision = "1"
            StateManager.get_state = MagicMock(return_value=state)
            StateRecovery.recover_from_post_data = MagicMock()
            questionnaire_manager = QuestionnaireManagerFactory.get_instance()
            StateRecovery.recover_from_post_data.assert_called_with(questionnaire_manager)

    def test_missing_revision_attribute(self):
        with self.application.test_request_context():
            state = self.mock_state()
            del state.revision
            StateManager.get_state = MagicMock(return_value=state)
            logger_name = 'app.questionnaire.questionnaire_manager_factory'
            logging.getLogger(logger_name).error = MagicMock()
            QuestionnaireManagerFactory.get_instance()
            logging.getLogger(logger_name).error.assert_called_with('Data not recoverable, old version of state without revision attribute')

    def mock_state(self):
        StateManager.has_state = MagicMock(return_value="True")
        node = Node("1", None)
        state = State(self.questionnaire, current_node=node, first_node=node, tail_node=node, valid_locations=[],
                    archive={}, submitted_at=None)
        return state
