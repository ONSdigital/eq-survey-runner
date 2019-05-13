from tests.integration.integration_test_case import IntegrationTestCase


class TestRenderDropdownWidget(IntegrationTestCase):
    def setUp(self, setting_overrides=None):
        super().setUp()
        self.launchSurvey('test', 'dropdown_mandatory')

    def test_dropdown_renders(self):
        self.assertInBody('Select an answer')
