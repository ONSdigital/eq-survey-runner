from app import settings
from tests.integration.integration_test_case import IntegrationTestCase


class TestApplicationVariables(IntegrationTestCase):

    def setUp(self):
        settings.EQ_ENABLE_FLASK_DEBUG_TOOLBAR = True
        settings.EQ_DEV_MODE = True
        settings.EQ_UA_ID = 'TestId'
        super().setUp()

    def tearDown(self):
        super().tearDown()
        settings.EQ_ENABLE_FLASK_DEBUG_TOOLBAR = False
        settings.EQ_DEV_MODE = False
        settings.EQ_UA_ID = None

    def test_flask_toolbar_is_displayed(self):
        self.launchSurvey('0', 'star_wars')
        self.assertStatusOK()
        self.assertInPage('flDebugToolbarHandle', 'The page does not contain the Flask toolbar')

    def test_google_analytics_code_is_present(self):
        self.launchSurvey('0', 'star_wars')
        self.assertStatusOK()
        self.assertInPage('GoogleAnalyticsObject', 'The page does not contain the GoogleAnalyticsObject')
