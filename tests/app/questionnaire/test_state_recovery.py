from app import settings
from app.questionnaire import state_recovery
from app.questionnaire.state_recovery import StateRecovery, POST_DATA, MAX_NO_OF_REPLAYS
from app.questionnaire.questionnaire_manager import QuestionnaireManager
from tests.app.framework.sr_unittest import SurveyRunnerTestCase
from app.authentication.user import QuestionnaireData
from unittest.mock import MagicMock

from flask_login import current_user
from werkzeug.datastructures import MultiDict, ImmutableMultiDict


class TestStateRecovery(SurveyRunnerTestCase):

    def test_save_post_data(self):
        with self.application.test_request_context():
            post_data = MultiDict()
            post_data.add("1", "test")
            location = "page1"

            StateRecovery.save_post_date(location, post_data)
            data_query = QuestionnaireData(current_user.user_id, current_user.user_ik)
            questionnaire_data = data_query.get_questionnaire_data()

            self.assertIsNotNone(questionnaire_data)
            self.assertEqual(post_data, questionnaire_data[POST_DATA][0]["post_data"])
            self.assertEqual(location, questionnaire_data[POST_DATA][0]["location"])

    def test_recover_from_post_data(self):
        with self.application.test_request_context():
            questionnaire_manager = QuestionnaireManager(self.questionnaire)
            questionnaire_manager.process_incoming_answers = MagicMock(return_value="page_2")
            questionnaire_manager.go_to = MagicMock()
            post_data = MultiDict()
            post_data.add("1", "test")
            post_data = ImmutableMultiDict(post_data)
            location = "page_1"

            StateRecovery.save_post_date(location, post_data)

            StateRecovery.recover_from_post_data(questionnaire_manager)
            questionnaire_manager.process_incoming_answers.assert_called_with(location, post_data, replay=True)
            questionnaire_manager.go_to.assert_called_with("page_2")

    def test_recover_from_post_data_replay_count(self):
        with self.application.test_request_context():
            setattr(state_recovery, "MAX_NO_OF_REPLAYS", 0)
            questionnaire_manager = QuestionnaireManager(self.questionnaire)
            questionnaire_manager.process_incoming_answers = MagicMock(return_value="page_2")
            questionnaire_manager.go_to = MagicMock()
            post_data = MultiDict()
            post_data.add("1", "test")
            post_data = ImmutableMultiDict(post_data)
            location = "page_1"

            StateRecovery.save_post_date(location, post_data)

            StateRecovery.recover_from_post_data(questionnaire_manager)
            questionnaire_manager.process_incoming_answers.assert_not_called()
            questionnaire_manager.go_to.assert_called_with("introduction")
            setattr(state_recovery, "MAX_NO_OF_REPLAYS", settings.EQ_MAX_REPLAY_COUNT)
