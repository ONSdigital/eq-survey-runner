from tests.integration.integration_test_case import IntegrationTestCase


class TestStatus(IntegrationTestCase):

    def test_status_page(self):
        self.get('/status')
        self.assertStatusOK()
        self.assertInPage('version')
