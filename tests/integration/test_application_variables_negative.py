from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase


class TestApplicationVariablesNegative(IntegrationTestCase):

    def setUp(self):
        IntegrationTestCase.setUp(self)

    def tearDown(self):
        IntegrationTestCase.tearDown(self)

    def test_flask_toolbar_is_not_displayed(self):

        token = create_token('star_wars', '0')
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=True)

        self.assertEqual(resp.status_code, 200)

        content = resp.get_data(True)

        self.assertFalse("flDebugToolbarHandle" in content, "The page contains the Flask toolbar")
