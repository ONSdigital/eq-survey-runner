from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireThankYou(IntegrationTestCase):

    def test_thank_you_unauthenticated(self):
        self.get('/questionnaire/test/0205/ce/thank-you')
        self.assertStatusUnauthorised()
