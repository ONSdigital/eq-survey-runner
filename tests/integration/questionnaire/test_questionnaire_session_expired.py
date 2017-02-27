from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase


class TestSessionExpired(IntegrationTestCase):

    def test_session_expired_should_log_user_out(self):
        # Given
        token = create_token('0205', '1')
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=False)

        # When
        self.client.get('/questionnaire/1/0205/789/session-expired')

        resp = self.client.get(resp.location)
        self.assertEqual(resp.status_code, 401)
