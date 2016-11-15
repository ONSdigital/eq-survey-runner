from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.mci import mci_test_urls


class TestQuestionnaireEndpointErrors(IntegrationTestCase):
    def test_get_invalid_questionnaire_location_shows_error_page(self):
        # Given
        token = create_token('0205', '1')
        self.client.get('/session?token=' + token.decode(), follow_redirects=False)

        # When
        resp = self.client.get(mci_test_urls.MCI_0205_BASE + 'some_group/0/test', follow_redirects=False)

        # Then
        self.assertEquals(resp.status_code, 404)
        self.assertRegex(resp.get_data(as_text=True), 'Error 404')
