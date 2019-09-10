from tests.integration.integration_test_case import IntegrationTestCase

class TestStatic(IntegrationTestCase):

    def test_contact(self):
        self.get('/contact-us')
        self.assertInBody('Contact us if you have any questions')

    def test_privacy(self):
        self.get('/privacy')
        self.assertInBody('Who can access the information?')
