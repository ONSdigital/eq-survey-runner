from app import settings
from tests.integration.integration_test_case import IntegrationTestCase


class TestApplicationVariables(IntegrationTestCase):

    def setUp(self):
        settings.EQ_ENABLE_FLASK_DEBUG_TOOLBAR = True
        settings.EQ_DEV_MODE = True
        settings.EQ_ENABLE_LIVE_RELOAD = True
        settings.EQ_GTM_ID = 'TestId'
        settings.EQ_GTM_ENV_ID = 'Dev'
        super().setUp()

    def tearDown(self):
        super().tearDown()
        settings.EQ_ENABLE_FLASK_DEBUG_TOOLBAR = False
        settings.EQ_DEV_MODE = False
        settings.EQ_ENABLE_LIVE_RELOAD = False
        settings.EQ_GTM_ID = None
        settings.EQ_GTM_ENV_ID = None

    def test_flask_toolbar_is_displayed(self):
        self.launchSurvey('0', 'star_wars')
        self.assertStatusOK()
        self.assertInBody('flDebugToolbarHandle')

    def test_livereload_script_rendered(self):
        self.launchSurvey('0', 'star_wars')
        self.assertStatusOK()
        self.assertTrue('__bs_script__' in self.getResponseData())
