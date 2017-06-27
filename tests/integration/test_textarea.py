from tests.integration.integration_test_case import IntegrationTestCase

class TestTextArea(IntegrationTestCase):


    def test_empty_sbmission(self):
        self.launchSurvey('test', 'textarea')
        self.post(action='save_continue')

        self.assertInPage('No answer provided')

        self.post(action=None)
        self.assertInUrl('thank-you')


    def test_too_many_characters(self):
        self.launchSurvey('test', 'textarea')
        self.post({'answer': "This is longer than twenty characters"})

        self.assertInPage('Your answer has to be less than 20 characters')

    def test_acceptable_submission(self):
        self.launchSurvey('test', 'textarea')
        self.post({'answer': "Less than 20 chars"})

        self.assertInPage("Less than 20 chars")

        self.post(action=None)
        self.assertInUrl('thank-you')
