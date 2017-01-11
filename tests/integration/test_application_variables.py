from app import settings
from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase


class TestApplicationVariables(IntegrationTestCase):

    def setUp(self):
        settings.EQ_ENABLE_FLASK_DEBUG_TOOLBAR = True
        settings.EQ_UA_ID = 'TestId'
        IntegrationTestCase.setUp(self)

    def tearDown(self):
        settings.EQ_ENABLE_FLASK_DEBUG_TOOLBAR = False
        IntegrationTestCase.tearDown(self)

    def test_flask_toolbar_is_displayed(self):

        token = create_token('star_wars', '0')
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=True)

        self.assertEqual(resp.status_code, 200)

        content = resp.get_data(True)

        self.assertTrue("flDebugToolbarHandle" in content, "The page does not contain the Flask toolbar")

    def test_google_analytics_code_is_present(self):

        token = create_token('star_wars', '0')
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=True)

        self.assertEqual(resp.status_code, 200)

        content = resp.get_data(True)

        self.assertTrue("GoogleAnalyticsObject" in content, "The page does not contain the GoogleAnalyticsObject")
