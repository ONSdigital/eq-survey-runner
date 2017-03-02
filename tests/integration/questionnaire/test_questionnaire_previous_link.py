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
        # Given
        token = create_token('final_confirmation', 'test')
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=True)

        # When
        # We proceed through the questionnaire
        post_data = {
            'csrf_token': self.extract_csrf_token(resp.get_data(True)),
            'action[start_questionnaire]': 'Start Questionnaire'
        }

        block_one_url, resp = self.postRedirectGet('/questionnaire/test/final_confirmation/789/final-confirmation/0/introduction', post_data)

        content = resp.get_data(True)
        self.assertIn('Previous', content)

        post_data = {
            'csrf_token': self.extract_csrf_token(resp.get_data(True)),
            "choose-your-side-answer": " Bacon",
            "action[save_continue]": "Save &amp; Continue"
        }
        resp_url, resp = self.postRedirectGet(block_one_url, post_data)

        content = resp.get_data(True)
        self.assertFalse(resp_url.endswith('thank-you'))
        self.assertIn('Previous', content)

    def test_previous_link_doesnt_appear_on_thank_you(self):
        # Given
        token = create_token('final_confirmation', 'test')
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=True)

        # When
        # We proceed through the questionnaire
        post_data = {
            'csrf_token': self.extract_csrf_token(resp.get_data(True)),
            'action[start_questionnaire]': 'Start Questionnaire'
        }

        block_one_url, resp = self.postRedirectGet('/questionnaire/test/final_confirmation/789/final-confirmation/0/introduction', post_data)

        post_data = {
            'csrf_token': self.extract_csrf_token(resp.get_data(True)),
            "choose-your-side-answer": " Bacon",
            "action[save_continue]": "Save and continue"
        }
        resp_url, resp = self.postRedirectGet(block_one_url, post_data)

        post_data = {
            "action[save_continue]": "Submit answers"
        }

        resp = self.get_and_post_with_csrf_token(resp_url, post_data)

        self.assertTrue(resp.location.endswith('thank-you'))

        resp = self.client.get(resp.location, follow_redirects=True)
        content = resp.get_data(True)
        self.assertNotIn('Previous', content)

    def test_previous_link_on_relationship(self):

        # Given the census questionnaire.
        self.token = create_token('household', 'census')
        self.client.get('/session?token=' + self.token.decode(), follow_redirects=True)

        # When we complete the who lives here section and the other questions needed to build the path.
        post_data = {
            'permanent-or-family-home-answer': 'Yes'
        }

        self.get_and_post_with_csrf_token('/questionnaire/census/household/789/who-lives-here/0/permanent-or-family-home', data=post_data)

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

        self.get_and_post_with_csrf_token('/questionnaire/census/household/789/who-lives-here/0/household-composition', data=post_data, follow_redirects=True)

        post_data = {
            'overnight-visitors-answer': '0'
        }
        resp = self.get_and_post_with_csrf_token('questionnaire/census/household/789/who-lives-here/0/overnight-visitors', data=post_data, follow_redirects=True)

        # Then there should be a previous link on all repeating household blocks.
        content = resp.get_data(True)
        self.assertIn('Previous', content)

        resp = self.client.get('questionnaire/census/household/789/who-lives-here-relationship/1/household-relationships')
        content = resp.get_data(True)
        self.assertIn('Previous', content)

