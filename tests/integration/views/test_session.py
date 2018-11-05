import time

from tests.integration.integration_test_case import IntegrationTestCase


class TestSession(IntegrationTestCase):
    def test_session_expired(self):
        self.get('/session-expired')
        self.assertInBody('Your session has expired')

    def test_session_signed_out(self):
        self.get('/signed-out')
        self.assertInBody('Your survey answers have been saved')

    def test_session_signed_out_with_overridden_account_service_url(self):
        self.launchSurvey(account_service_url='https://ras.ons.gov.uk')
        self.get('/signed-out')
        self.assertInBody('Your survey answers have been saved')
        self.assertInBody('My account')
        self.assertInBody('Return to your account')
        self.assertInBody('https://ras.ons.gov.uk')

    def test_session_signed_out_with_none_overridden_account_service_url(self):
        self.launchSurvey(account_service_url=None)
        self.get('/signed-out')
        self.assertInBody('Your survey answers have been saved')
        self.assertNotInBody('My account')
        self.assertNotInBody('Return to your account')

    def test_session_jti_token_expired(self):
        self.launchSurvey(exp=time.time() - float(60))
        self.assertStatusUnauthorised()
