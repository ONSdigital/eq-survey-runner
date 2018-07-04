import time

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

    def test_session_signed_out_with_overridden_Account_url(self):
        self.launchSurvey(account_service_url='https://ras.ons.gov.uk')
        self.get('/signed-out')
        self.assertInPage('Your survey answers have been saved')
        self.assertNotInPage(RESPONDENT_ACCOUNT_URL)
        self.assertInPage('https://ras.ons.gov.uk')

    def test_session_signed_out_with_none_overridden_Account_url(self):
        self.launchSurvey(account_service_url=None)
        self.get('/signed-out')
        self.assertInPage('Your survey answers have been saved')
        self.assertInPage(RESPONDENT_ACCOUNT_URL)

    def test_session_jti_token_expired(self):
        self.launchSurvey(exp=time.time() - float(60))
        self.assertStatusUnauthorised()
