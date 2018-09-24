import time

from tests.integration.integration_test_case import IntegrationTestCase


class TestSession(IntegrationTestCase):
    def test_session_expired(self):
        self.get('/session-expired')
        self.assertInPage('Your session has expired')

    def test_session_signed_out(self):
        self.get('/signed-out')
        self.assertInPage('Your survey answers have been saved')

    def test_session_signed_out_with_overridden_account_service_url(self):
        self.launchSurvey(account_service_url='https://ras.ons.gov.uk')
        self.get('/signed-out')
        self.assertInPage('Your survey answers have been saved')
        self.assertInPage('My account')
        self.assertInPage('Return to your account')
        self.assertInPage('https://ras.ons.gov.uk')

    def test_session_signed_out_with_none_overridden_account_service_url(self):
        self.launchSurvey(account_service_url=None)
        self.get('/signed-out')
        self.assertInPage('Your survey answers have been saved')
        self.assertNotInPage('My account')
        self.assertNotInPage('Return to your account')

    def test_session_jti_token_expired(self):
        self.launchSurvey(exp=time.time() - float(60))
        self.assertStatusUnauthorised()
