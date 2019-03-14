import simplejson as json
from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireJSONOutput(IntegrationTestCase):

    def test_questionnaire_json_response(self):

        # Given
        self.launchSurvey('test', 'final_confirmation')

        # When
        self.get('/questionnaire/introduction', headers={'Accept': 'application/json'})

        # Then
        data = json.loads(self.getResponseData())
        self.assertIn('block', data)
