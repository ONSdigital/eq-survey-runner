from tests.integration.integration_test_case import IntegrationTestCase


class TestMultipleSurveyError(IntegrationTestCase):

    def test_different_metadata_store_to_url(self):
        # Launch a first questionnaire
        self.launchSurvey('test', '0205')
        self.assertInBody('>Start survey<')
        self.assertInBody('Monthly Business Survey - Retail Sales Index')

        # Remember url for later
        first_url = self.last_url

        # Launch a second questionnaire
        self.launchSurvey('0', 'star_wars')
        self.assertInBody('>Start survey<')
        self.assertInBody('Star Wars')

        # We try to post to the wrong questionnaire
        self.post(url=first_url, action='start_questionnaire')
        self.assertInBody('Information')
        self.assertInBody('Unfortunately you can only complete one survey at a time.')
        self.assertInBody('Close this window to continue with your current survey.')
