from app import settings
from tests.integration.integration_test_case import IntegrationTestCase


class TestApplicationVariablesNegative(IntegrationTestCase):

    def setUp(self):
        settings.EQ_DEV_MODE = True
        settings.EQ_ENABLE_LIVE_RELOAD = False
        super().setUp()

    def test_flask_toolbar_is_not_displayed(self):
        self.launchSurvey('0', 'star_wars')
        self.assertStatusOK()
        self.assertNotInBody('flDebugToolbarHandle')

    def test_livereload_script_not_rendered(self):
        self.launchSurvey('0', 'star_wars')
        self.assertStatusOK()
        self.assertFalse('__bs_script__' in self.getResponseData())
