from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnairePreviousLink(IntegrationTestCase):

    def test_previous_link_doesnt_appear_on_introduction(self):
        # Given
        token = create_token('final_confirmation', 'test')
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=False)

        # When we open the introduction
        content = resp.get_data(True)

        # Then previous link does not appear
        self.assertNotIn('Previous', content)

    def test_previous_link_appears_on_page_following_introduction(self):
        base_url = '/questionnaire/test/final_confirmation/789/'

        # Given
        token = create_token('final_confirmation', 'test')
        self.client.get('/session?token=' + token.decode(), follow_redirects=False)

        # When
        # We proceed through the questionnaire
        post_data = {
            'action[start_questionnaire]': 'Start Questionnaire'
        }

        block_one_url, resp = self.postRedirectGet(base_url + 'introduction', post_data)

        content = resp.get_data(True)
        self.assertNotRegex(content, 'Previous')

        post_data = {
            "ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c": " Bacon",
            "action[save_continue]": "Save &amp; Continue"
        }
        resp_url, resp = self.postRedirectGet(block_one_url, post_data)

        content = resp.get_data(True)
        self.assertFalse(resp_url.endswith('thank-you'))
        self.assertIn('Previous', content)

    def test_previous_link_doesnt_appear_on_thank_you(self):
        base_url = '/questionnaire/test/final_confirmation/789/'

        # Given
        token = create_token('final_confirmation', 'test')
        self.client.get('/session?token=' + token.decode(), follow_redirects=False)

        # When
        # We proceed through the questionnaire
        post_data = {
            'action[start_questionnaire]': 'Start Questionnaire'
        }

        block_one_url, resp = self.postRedirectGet(base_url + 'introduction', post_data)

        post_data = {
            "ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c": " Bacon",
            "action[save_continue]": "Save and continue"
        }
        self.postRedirectGet(block_one_url, post_data)

        post_data = {
            "action[save_continue]": "Submit answers"
        }

        final_url, resp = self.postRedirectGet(base_url + 'submit-answers', post_data)

        content = resp.get_data(True)
        self.assertTrue(final_url.endswith('thank-you'))
        self.assertNotIn('Previous', content)

