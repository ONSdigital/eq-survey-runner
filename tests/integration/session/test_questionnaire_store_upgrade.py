from unittest.mock import patch
from tests.integration.integration_test_case import IntegrationTestCase

class TestLogin(IntegrationTestCase):

    def test_questionnaire_store_is_upgraded(self):
        # Given

        # Creates a QuestionnaireStore with a version of 0
        with patch('app.data_model.questionnaire_store.QuestionnaireStore.get_latest_version_number', return_value=0):
            self.launchSurvey('test', '0205')

        # LATEST_VERSION is now > 0 (it was 1 at time of writing), so the `upgrade` method
        # of answer_store should be called when fetching the questionnaire_store
        with patch('app.data_model.questionnaire_store.AnswerStore.upgrade') as upgrade:
            self.post(action='start_questionnaire')

        upgrade.assert_called_once()
