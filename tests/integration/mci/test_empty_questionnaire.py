from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.create_token import create_token


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
        self.assertRegexpMatches(content, '>Get Started<')

        # We try to access the submission page without entering anything
        resp = self.client.get('/questionnaire/1\/789\/summary', follow_redirects=False)
        self.assertEquals(resp.status_code, 302)

        # Check we are redirected back to the questionnaire
        self.assertRegexpMatches(resp.headers['Location'], 'introduction')

        # We try posting to the submission page without our answers
        post_data = {
            'action[submit_answers]': "Submit Answers"
        }
        resp = self.client.post('/questionnaire/1/789/summary', data=post_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)

        # Check we are redirected back to the questionnaire
        self.assertRegexpMatches(resp.headers['Location'], 'introduction')
