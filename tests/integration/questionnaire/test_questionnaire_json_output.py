import simplejson as json
from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireJSONOutput(IntegrationTestCase):

    def test_questionnaire_json_response(self):

        # Given
        self.launchSurvey('test', 'final_confirmation')

        # When
        #import ipdb; ipdb.set_trace()
        self.get('/questionnaire/test/final_confirmation/789/final-confirmation/0/introduction', headers={'Accept': 'application/json'})

        # Then
        data = json.loads(self.getResponseData())
        self.assertIn('block', data)
