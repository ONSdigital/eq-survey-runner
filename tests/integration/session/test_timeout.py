import time

from app import settings
from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase


class TestTimeout(IntegrationTestCase):

    def setUp(self):
        settings.EQ_SESSION_TIMEOUT_SECONDS = 1
        settings.EQ_SESSION_TIMEOUT_GRACE_PERIOD_SECONDS = 0
        IntegrationTestCase.setUp(self)

    def test_timeout_continue_returns_200(self):
        # Given
        token = create_token('timeout', 'test')

        # When
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=False)

        # Then
        self.assertEqual(resp.status_code, 302)

        resp = self.client.get('/questionnaire/test/timeout/789/timeout-continue', follow_redirects=False)
        self.assertEqual(resp.status_code, 200)

    def test_session_expired_clears_session(self):
        # Given
        token = create_token('timeout', 'test')

        # When
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=False)

        # Then
        self.assertEqual(resp.status_code, 302)

        resp = self.client.get('/questionnaire/test/timeout/789/session-expired', follow_redirects=False)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/questionnaire/test/timeout/789/session-expired', follow_redirects=False)
        self.assertEqual(resp.status_code, 401)

    def test_when_session_times_out_server_side_401_is_returned(self):
        # Given
        token = create_token('timeout', 'test')

        # When
        login_resp = self.client.get('/session?token=' + token.decode(), follow_redirects=False)

        # Then
        self.assertEqual(login_resp.status_code, 302)

        resp = self.client.get(login_resp.location, follow_redirects=False)
        self.assertEqual(resp.status_code, 200)

        time.sleep(2)

        resp = self.client.get(login_resp.location, follow_redirects=False)
        self.assertEqual(resp.status_code, 401)

    def test_schema_defined_timeout_is_used(self):
        # Given
        settings.EQ_SESSION_TIMEOUT_SECONDS = 10
        token = create_token('timeout', 'test')

        # When
        login_resp = self.client.get('/session?token=' + token.decode(), follow_redirects=False)

        # Then
        resp = self.client.get(login_resp.location, follow_redirects=False)
        self.assertEqual(resp.status_code, 200)

        content = resp.get_data(True)
        self.assertIn('window.__EQ_SESSION_TIMEOUT__ = 4', content)

    def test_schema_defined_timeout_cant_be_higher_than_server(self):
        # Given
        token = create_token('timeout', 'test')

        # When
        login_resp = self.client.get('/session?token=' + token.decode(), follow_redirects=False)

        # Then
        resp = self.client.get(login_resp.location, follow_redirects=False)
        self.assertEqual(resp.status_code, 200)

        content = resp.get_data(True)
        self.assertIn('window.__EQ_SESSION_TIMEOUT__ = 1', content)
