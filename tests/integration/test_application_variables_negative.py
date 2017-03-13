from app import settings
from tests.integration.integration_test_case import IntegrationTestCase


class TestApplicationVariablesNegative(IntegrationTestCase):

    def setUp(self):
        settings.EQ_DEV_MODE = True
        super().setUp()

    def test_flask_toolbar_is_not_displayed(self):
        self.launchSurvey('0', 'star_wars')
        self.assertStatusOK()
        self.assertNotInPage('flDebugToolbarHandle', 'The page contains the Flask toolbar')
