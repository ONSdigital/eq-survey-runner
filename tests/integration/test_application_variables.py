from app import settings
from tests.integration.integration_test_case import IntegrationTestCase


class TestApplicationVariables(IntegrationTestCase):
    def setUp(self):
        settings.EQ_ENABLE_FLASK_DEBUG_TOOLBAR = True
        settings.EQ_DEV_MODE = True
        settings.EQ_ENABLE_LIVE_RELOAD = True
        settings.EQ_GOOGLE_TAG_MANAGER_ID = 'TestId'
        settings.EQ_GOOGLE_TAG_MANAGER_AUTH = 'TestAuth'
        settings.EQ_GOOGLE_TAG_MANAGER_PREVIEW = 'TestPreview'
        super().setUp()

    def tearDown(self):
        super().tearDown()
        settings.EQ_ENABLE_FLASK_DEBUG_TOOLBAR = False
        settings.EQ_DEV_MODE = False
        settings.EQ_ENABLE_LIVE_RELOAD = False
        settings.EQ_GOOGLE_TAG_MANAGER_ID = None
        settings.EQ_GOOGLE_TAG_MANAGER_AUTH = None
        settings.EQ_GOOGLE_TAG_MANAGER_PREVIEW = None

    def test_flask_toolbar_is_displayed(self):
        self.launchSurvey('test', 'textfield')
        self.assertStatusOK()
        self.assertInBody('flDebugToolbarHandle')

    def test_google_analytics_code_is_present(self):
        self.launchSurvey('test', 'textfield')
        self.assertStatusOK()
        self.assertInHead('gtm.start')
        self.assertInHead('dataLayer = [];')
        self.assertInBody('https://www.googletagmanager.com')

    def test_livereload_script_rendered(self):
        self.launchSurvey('test', 'textfield')
        self.assertStatusOK()
        self.assertTrue('__bs_script__' in self.getResponseData())
