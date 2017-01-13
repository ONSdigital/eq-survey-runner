from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.mci import mci_test_urls


class TestEmptyQuestionnaire(IntegrationTestCase):

    def test_empty_questionnaire(self):
        # Get a token
        token = create_token('0205', '1')
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=False)
        self.assertEqual(resp.status_code, 302)
        intro_page_url = resp.location

        # Navigate to the Introduction Page
        resp = self.client.get(intro_page_url, follow_redirects=False)
        self.assertEqual(resp.status_code, 200)

        # We are on the landing page
        content = resp.get_data(True)
        self.assertRegex(content, '>Start survey<')

        post_data = {
            'action[start_questionnaire]': "Submit Answers"
        }

        # Submit the Introduction page to get the first question page
        resp = self.client.post(intro_page_url, data=post_data, follow_redirects=False)
        self.assertEqual(resp.status_code, 302)

        first_question_page = resp.location

        # We try to access the submission page without entering anything
        resp = self.client.get(mci_test_urls.MCI_0205_SUMMARY, follow_redirects=False)
        self.assertEqual(resp.status_code, 302)

        # Check we are redirected back to the questionnaire
        self.assertEqual(resp.location, first_question_page)

        # We try posting to the submission page without our answers
        post_data = {
            'action[submit_answers]': "Submit Answers"
        }
        resp = self.client.post(mci_test_urls.MCI_0205_SUBMIT, data=post_data, follow_redirects=False)
        self.assertEqual(resp.status_code, 302)

        # Check we are redirected back to the questionnaire
        self.assertEqual(resp.location, first_question_page)
