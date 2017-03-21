from tests.integration.integration_test_case import IntegrationTestCase


class TestSessionExpired(IntegrationTestCase):

    def test_session_expired_should_log_user_out(self):
        self.launchSurvey('1', '0205')
        self.get('/questionnaire/1/0205/789/session-expired')
        self.assertStatusOK()
        self.get('/questionnaire/1/0205/789/session-expired')
        self.assertStatusUnauthorised()
