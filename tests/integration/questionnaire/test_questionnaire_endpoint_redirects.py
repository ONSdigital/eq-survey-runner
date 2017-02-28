from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.mci import mci_test_urls


class TestQuestionnaireEndpointRedirects(IntegrationTestCase):
    def test_get_invalid_questionnaire_location_redirects_to_latest(self):
        # Given
        token = create_token('0205', '1')
        self.client.get('/session?token=' + token.decode(), follow_redirects=False)

        # When
        resp = self.client.get(mci_test_urls.MCI_0205_BASE + 'test', follow_redirects=False)

        # Then
        self.assertEqual(resp.status_code, 302)
        self.assertIn(mci_test_urls.MCI_0205_INTRODUCTION, resp.location)

    def test_post_invalid_questionnaire_location_redirects_to_latest(self):
        # Given
        token = create_token('0205', '1')
        self.client.get('/session?token=' + token.decode(), follow_redirects=False)

        # When
        resp = self.client.post(mci_test_urls.MCI_0205_BASE + 'test', follow_redirects=False)

        # Then
        self.assertEqual(resp.status_code, 302)
        self.assertIn(mci_test_urls.MCI_0205_INTRODUCTION, resp.location)

    def test_submit_answers_for_invalid_questionnaire_location_redirects_to_first_incomplete_location(self):
        # Given
        token = create_token('0205', '1')
        self.client.get('/session?token=' + token.decode(), follow_redirects=False)

        # When
        resp = self.client.post(mci_test_urls.MCI_0205_SUMMARY, follow_redirects=False)

        # Then
        self.assertEqual(resp.status_code, 302)
        self.assertIn(mci_test_urls.MCI_0205_INTRODUCTION, resp.location)
