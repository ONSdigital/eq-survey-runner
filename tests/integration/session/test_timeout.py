import time

from app import settings
from tests.integration.integration_test_case import IntegrationTestCase


class TestTimeout(IntegrationTestCase):
    def setUp(self):
        settings.EQ_SESSION_TIMEOUT_SECONDS = 2
        super().setUp()

    def tearDown(self):
        settings.EQ_SESSION_TIMEOUT_SECONDS = 45 * 60
        super().tearDown()

    def test_timeout_continue_valid_session_returns_200(self):
        self.launchSurvey('test_timeout')
        self.get(self.last_url)
        self.assertStatusOK()

    def test_when_session_times_out_server_side_401_is_returned(self):
        self.launchSurvey('test_timeout')
        time.sleep(3)
        self.get(self.last_url)
        self.assertStatusUnauthorised()

    def test_schema_defined_timeout_cant_be_higher_than_server(self):
        self.launchSurvey('test_timeout')
        time.sleep(2)
        self.get(self.last_url)
        self.assertStatusUnauthorised()
