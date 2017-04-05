from tests.integration.integration_test_case import IntegrationTestCase


class TestSessionExpired(IntegrationTestCase):

    def test_session_expired_should_log_user_out(self):
        self.launchSurvey('1', '0205')
        self.post(url='/questionnaire/1/0205/789/expire-session')
        self.assertStatusOK()
        self.post(url='/questionnaire/1/0205/789/expire-session')
        self.assertStatusUnauthorised()
