from tests.integration.integration_test_case import IntegrationTestCase


class TestSessionExpired(IntegrationTestCase):

    def test_session_expired_should_log_user_out(self):
        self.launchSurvey('1', '0205')
        start_page = self.last_url
        self.post(url='/expire-session')
        self.assertStatusOK()
        self.get(url=start_page)
        self.assertStatusUnauthorised()
