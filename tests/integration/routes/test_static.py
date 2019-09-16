from tests.integration.integration_test_case import IntegrationTestCase


class TestStatic(IntegrationTestCase):
    def test_privacy(self):
        self.get('/privacy')
        self.assertInBody('Who can access the information?')
