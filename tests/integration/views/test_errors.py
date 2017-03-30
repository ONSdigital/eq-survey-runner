from tests.integration.integration_test_case import IntegrationTestCase


class TestErrors(IntegrationTestCase):

    def test_errors_404(self):
        self.get('/hfjdskahfjdkashfsa')
        self.assertStatusNotFound()
        self.assertInPage('Error 404')
