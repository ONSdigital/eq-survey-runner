from tests.integration.integration_test_case import IntegrationTestCase


class TestApplicationVariables(IntegrationTestCase):
    def setUp(self, setting_overrides=None):
        super().setUp({
            'EQ_ENABLE_FLASK_DEBUG_TOOLBAR': True,
            'EQ_DEV_MODE': True,
            'EQ_ENABLE_LIVE_RELOAD': True,
            'EQ_UA_ID': 'TestId'
        })

    def test_flask_toolbar_is_displayed(self):
        self.launchSurvey('test', 'textfield')
        self.assertStatusOK()
        self.assertInBody('flDebugToolbarHandle')

    def test_google_analytics_code_is_present(self):
        self.launchSurvey('test', 'textfield')
        self.assertStatusOK()
        self.assertInBody('GoogleAnalyticsObject')

    def test_livereload_script_rendered(self):
        self.launchSurvey('test', 'textfield')
        self.assertStatusOK()
        self.assertTrue('__bs_script__' in self.getResponseData())
