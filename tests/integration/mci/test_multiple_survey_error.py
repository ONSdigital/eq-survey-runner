from tests.integration.integration_test_case import IntegrationTestCase


class TestMultipleSurveyError(IntegrationTestCase):

    def test_different_metadata_store_to_url(self):
        # Launch a first questionnaire
        self.launchSurvey('1', '0205')
        self.assertInPage('>Start survey<')
        self.assertInPage('Monthly Business Survey - Retail Sales Index')

        # Remember url for later
        first_url = self.last_url

        # Launch a second questionnaire
        self.launchSurvey('0', 'star_wars')
        self.assertInPage('>Start survey<')
        self.assertInPage('Star Wars')

        # We try to post to the wrong questionnaire
        self.post(url=first_url, action='start_questionnaire')
        self.assertInPage('Information')
        self.assertInPage('Unfortunately you can only complete one survey at a time.')
        self.assertInPage('Close this window to continue with your current survey.')
