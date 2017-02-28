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
        base_url = '/questionnaire/test/final_confirmation/789/14ba4707-321d-441d-8d21-b8367366e766/0/'

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
        self.assertIn('Previous', content)

        post_data = {
            "ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c": " Bacon",
            "action[save_continue]": "Save &amp; Continue"
        }
        resp_url, resp = self.postRedirectGet(block_one_url, post_data)

        content = resp.get_data(True)
        self.assertFalse(resp_url.endswith('thank-you'))
        self.assertIn('Previous', content)

    def test_previous_link_doesnt_appear_on_thank_you(self):
        base_url = '/questionnaire/test/final_confirmation/789/14ba4707-321d-441d-8d21-b8367366e766/0/'

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

        final_url, resp = self.postRedirectGet('/questionnaire/test/final_confirmation/789/submit-answers', post_data)

        content = resp.get_data(True)
        self.assertTrue(final_url.endswith('thank-you'))
        self.assertNotIn('Previous', content)

    def test_previous_link_on_relationship(self):

        # Given the census questionnaire.
        self.token = create_token('household', 'census')
        self.client.get('/session?token=' + self.token.decode(), follow_redirects=True)

        # When we complete the who lives here section and the other questions needed to build the path.
        post_data = {
            'permanent-or-family-home-answer': 'Yes'
        }

        self.client.post('/questionnaire/census/household/789/who-lives-here/0/permanent-or-family-home', data=post_data)

        post_data = {
            'household-0-first-name': 'Joe',
            'household-0-middle-names': '',
            'household-0-last-name': 'Bloggs',
            'household-1-first-name': 'Jane',
            'household-1-middle-names': '',
            'household-1-last-name': 'Bloggs',
            'household-2-first-name': 'Holly',
            'household-2-middle-names': '',
            'household-2-last-name': 'Bloggs',
        }

        self.client.post('/questionnaire/census/household/789/who-lives-here/0/household-composition', data=post_data, follow_redirects=True)

        post_data = {
            'overnight-visitors-answer': '0'
        }
        resp = self.client.post('questionnaire/census/household/789/who-lives-here/0/overnight-visitors', data=post_data, follow_redirects=True)

        # Then there should be a previous link on all repeating household blocks.
        content = resp.get_data(True)
        self.assertIn('Previous', content)

        resp = self.client.get('questionnaire/census/household/789/who-lives-here-relationship/1/household-relationships')
        content = resp.get_data(True)
        self.assertIn('Previous', content)

