from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireInterstitial(IntegrationTestCase):

    BASE_URL = '/questionnaire/test/interstitial_page/789/'

    def test_form_not_processed_with_no_csrf_token(self):
        token = create_token('interstitial_page', 'test')
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=True)

        post_data = {
            'action[start_questionnaire]': 'Start survey'
        }

        resp = self.client.post(self.BASE_URL + 'favourite-foods/0/introduction', post_data)

        self.assertEquals(200, resp.status_code)

    def test_form_not_processed_with_incorrect_csrf_token(self):
        token = create_token('interstitial_page', 'test')
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=True)

        post_data = {
            'csrf_token': 'made-up-token',
            'action[start_questionnaire]': 'Start survey'
        }

        resp = self.client.post(self.BASE_URL + 'favourite-foods/0/introduction', post_data)

        self.assertEquals(200, resp.status_code)

    def test_form_processed_with_correct_csrf_token(self):
        token = create_token('interstitial_page', 'test')
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=True)

        post_data = {
            'action[start_questionnaire]': 'Start survey'
        }

        resp = self.get_and_post_with_csrf_token(self.BASE_URL + 'favourite-foods/0/introduction', post_data)

        self.assertEquals(302, resp.status_code)

