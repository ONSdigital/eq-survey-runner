from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireInterstitial(IntegrationTestCase):

    BASE_URL = '/questionnaire/'

    def test_interstitial_page_button_text_is_continue(self):
        self.launchSurvey('test', 'interstitial_page')
        self.post(action='start_questionnaire')
        self.post({'favourite-breakfast': 'Cereal'})
        self.assertInBody('Continue')

    def test_interstitial_page_can_continue_and_submit(self):
        self.launchSurvey('test', 'interstitial_page')
        self.post(action='start_questionnaire')
        self.post({'favourite-breakfast': 'Cereal'})
        self.post(action='save_continue')
        self.assertInUrl('lunch-block')
        self.post({'favourite-lunch': 'Pizza'})
        self.assertInUrl('confirmation')
        self.post(action=None)
        self.assertInBody('Submission successful')
