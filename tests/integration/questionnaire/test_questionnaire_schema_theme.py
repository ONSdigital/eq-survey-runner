from tests.integration.integration_test_case import IntegrationTestCase


class TestSchemaTheme(IntegrationTestCase):

    BASE_URL = '/questionnaire/'

    def test_interstitial_can_continue_and_submit_census(self):
        self.launchSurvey('test_theme_census')
        self.assertInUrl('name-block')
        self.post({'name': 'Pete'})
        self.assertInUrl('confirmation')
        self.post(action=None)
        self.assertInBody('Thank you for submitting your census')
