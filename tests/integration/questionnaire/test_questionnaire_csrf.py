from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireInterstitial(IntegrationTestCase):

    def setUp(self):
        super().setUp()
        self.launchSurvey('test', 'interstitial_page')
        self.assertInPage('Your response is legally required')
        self.first_url = self.last_url

    def test_form_not_processed_with_no_csrf_token(self):
        self.last_csrf_token = None
        self.post(action='start_questionnaire')
        self.assertStatusOK()
        self.assertEqualUrl(self.first_url)

    def test_form_not_processed_with_incorrect_csrf_token(self):
        self.last_csrf_token = 'made-up-token'
        self.post(action='start_questionnaire')
        self.assertStatusOK()
        self.assertEqualUrl(self.first_url)

    def test_form_processed_with_correct_csrf_token(self):
        self.post(action='start_questionnaire')
        self.assertStatusOK()
        self.assertInPage('What is your favourite breakfast food')
