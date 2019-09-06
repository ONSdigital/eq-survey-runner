import time

from tests.integration.integration_test_case import IntegrationTestCase


class TestSession(IntegrationTestCase):
    def test_session_expired(self):
        self.get('/session-expired')
        self.assertInBody('Your session has expired')

    def test_session_signed_out(self):

        self.launchSurvey(account_service_log_out_url='https://localhost/logout')
        self.assertInBody('Save and sign out')

        self.post(action='save_sign_out')

        self.assertInUrl('/logout')

    def test_session_jti_token_expired(self):
        self.launchSurvey(exp=time.time() - float(60))
        self.assertStatusUnauthorised()
