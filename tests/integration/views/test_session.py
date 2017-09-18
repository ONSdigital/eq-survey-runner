from tests.integration.integration_test_case import IntegrationTestCase


class TestSession(IntegrationTestCase):

    def test_session_expired(self):
        self.get('/session-expired')
        self.assertInPage('Your session has expired')

    def test_session_signed_out(self):
        self.get('/signed-out')
        self.assertInPage('Your survey has been saved')
