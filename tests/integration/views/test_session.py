from tests.integration.integration_test_case import IntegrationTestCase
from app.settings import RESPONDENT_ACCOUNT_URL


class TestSession(IntegrationTestCase):
    def test_session_expired(self):
        self.get('/session-expired')
        self.assertInPage('Your session has expired')

    def test_session_signed_out(self):
        self.get('/signed-out')
        self.assertInPage('Your survey answers have been saved')
        self.assertInPage(RESPONDENT_ACCOUNT_URL)
