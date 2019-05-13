from tests.integration.integration_test_case import IntegrationTestCase


class TestApplicationVariablesNegative(IntegrationTestCase):
    def setUp(self, setting_overrides=None):
        super().setUp({'EQ_DEV_MODE': True, 'EQ_ENABLE_LIVE_RELOAD': False})

    def test_flask_toolbar_is_not_displayed(self):
        self.launchSurvey('test', 'textfield')
        self.assertStatusOK()
        self.assertNotInBody('flDebugToolbarHandle')

    def test_livereload_script_not_rendered(self):
        self.launchSurvey('test', 'textfield')
        self.assertStatusOK()
        self.assertFalse('__bs_script__' in self.getResponseData())
