from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.mci import mci_test_urls


class TestEmptyQuestionnaire(IntegrationTestCase):

    def test_empty_questionnaire(self):
        # Get a token
        token = create_token('0205', '1')
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=False)
        self.assertEquals(resp.status_code, 302)
        intro_page_url = resp.headers['Location']

        # We try to access the submission page without entering anything
        resp = self.client.get(intro_page_url, follow_redirects=False)
        self.assertEquals(resp.status_code, 200)

        # We are on the landing page
        content = resp.get_data(True)
        self.assertRegexpMatches(content, '>Start survey<')

        # We try to access the submission page without entering anything
        resp = self.client.get(mci_test_urls.MCI_0205_SUMMARY, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)

        # Check we are redirected back to the questionnaire
        self.assertRegexpMatches(resp.headers['Location'], 'introduction')

        # We try posting to the submission page without our answers
        post_data = {
            'action[submit_answers]': "Submit Answers"
        }
        resp = self.client.post(mci_test_urls.MCI_0205_SUMMARY, data=post_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)

        # Check we are redirected back to the questionnaire
        self.assertRegexpMatches(resp.headers['Location'], 'introduction')
