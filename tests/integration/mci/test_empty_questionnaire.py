from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.create_token import create_token


class TestEmptyQuestionnaire(IntegrationTestCase):

    def test_empty_questionnaire(self):
        # Get a token
        token = create_token('0205', '1')
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=True)
        self.assertEquals(resp.status_code, 200)

        # We are on the landing page
        content = resp.get_data(True)
        self.assertRegexpMatches(content, '>Get Started<')

        # # We proceed to the questionnaire
        # resp = self.client.get('/questionnaire/1/789/cd3b74d1-b687-4051-9634-a8f9ce10a27d', follow_redirects=True)
        # self.assertEquals(resp.status_code, 200)
        #
        # # We are in the Questionnaire
        # content = resp.get_data(True)
        # self.assertRegexpMatches(content, "What are the dates of the sales period you are reporting for\?")
        
        # We try to access the submission page without entering anything
        resp = self.client.get('/questionnaire/1\/789\/summary', follow_redirects=True)
        self.assertEquals(resp.status_code, 200)

        # We submit our answers
        post_data = {
            'action[submit_answers]': "Submit Answers"
        }
        resp = self.client.post('/questionnaire/1/789/summary', data=post_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)
        self.assertRegexpMatches(resp.headers['Location'], '\/questionnaire\/1\/789\/thank-you$')
        resp = self.client.get(resp.headers['Location'], follow_redirects=True)
        self.assertEquals(resp.status_code, 200)

        # We are on the thank you page
        content = resp.get_data(True)
        self.assertRegexpMatches(content, '>Successfully Received<')
