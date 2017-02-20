import time

from app import settings
from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase


class TestTimeout(IntegrationTestCase):

    def setUp(self):
        settings.EQ_SESSION_TIMEOUT_SECONDS = 1
        IntegrationTestCase.setUp(self)

    def test_timeout_continue_returns_200(self):
        # Given
        token = create_token('0205', '1')

        # When
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=False)

        # Then
        self.assertEqual(resp.status_code, 302)

        resp = self.client.get('/questionnaire/1/0205/789/timeout-continue', follow_redirects=False)
        self.assertEqual(resp.status_code, 200)

    def test_session_expired_clears_session(self):
        # Given
        token = create_token('0205', '1')

        # When
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=False)

        # Then
        self.assertEqual(resp.status_code, 302)

        resp = self.client.get('/questionnaire/1/0205/789/session-expired', follow_redirects=False)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/questionnaire/1/0205/789/session-expired', follow_redirects=False)
        self.assertEqual(resp.status_code, 401)

    def test_when_session_times_out_server_side_401_is_returned(self):
        # Given
        token = create_token('0205', '1')

        # When
        login_resp = self.client.get('/session?token=' + token.decode(), follow_redirects=False)

        # Then
        self.assertEqual(login_resp.status_code, 302)

        resp = self.client.get(login_resp.location, follow_redirects=False)
        self.assertEqual(resp.status_code, 200)

        time.sleep(2)

        resp = self.client.get(login_resp.location, follow_redirects=False)
        self.assertEqual(resp.status_code, 401)
