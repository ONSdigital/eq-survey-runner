from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireFinalConfirmation(IntegrationTestCase):

    def test_final_confirmation_asked_at_end_of_questionnaire(self):
        base_url = '/questionnaire/test/final_confirmation/789/'

        # Given
        token = create_token('final_confirmation', 'test')
        self.client.get('/session?token=' + token.decode(), follow_redirects=False)

        # When
        # We proceed through the questionnaire
        post_data = {
            'action[start_questionnaire]': 'Start Questionnaire'
        }
        resp = self.client.post(base_url + 'introduction', data=post_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)

        block_one_url = resp.headers['Location']

        post_data = {
            "ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c": " Bacon",
            "action[save_continue]": "Save &amp; Continue"
        }
        resp = self.client.post(block_one_url, data=post_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)

        # Then
        # we are presented with a confirmation page
        self.assertTrue("confirmation" in resp.headers['Location'])
        self.assertEquals(resp.status_code, 302)

        resp = self.client.get(resp.headers['Location'], follow_redirects=False)
        self.assertEquals(resp.status_code, 200)


    def test_requesting_final_confirmation_before_finished_redirects(self):
        base_url = '/questionnaire/test/final_confirmation/789/'

        # Given
        token = create_token('final_confirmation', 'test')
        self.client.get('/session?token=' + token.decode(), follow_redirects=False)

        # When
        # We proceed through the questionnaire
        post_data = {
            'action[start_questionnaire]': 'Start Questionnaire'
        }
        resp = self.client.post(base_url + 'introduction', data=post_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)

        block_one_url = resp.headers['Location']

        resp = self.client.get(base_url + 'confirmation', follow_redirects=False)
        self.assertEquals(resp.headers['Location'], block_one_url)
        self.assertEquals(resp.status_code, 302)
