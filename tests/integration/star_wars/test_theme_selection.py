from .test_light_side_path import TestLightSidePath
from tests.integration.create_token import create_token


class TestThemeSelection(TestLightSidePath):
    """
    This test checks that we are using the Star wars theme as
    specified in the test survey schema.
    """


    def test_theme(self):
        """
        Theme Test case
        """
        token = create_token('star_wars', '0')
        resp = self.client.get('/session?token=' + token.decode(),
                               follow_redirects=True)
        self.assertEquals(resp.status_code, 200)

        # We are on the landing page
        content = resp.get_data(True)
        # We proceed to the questionnaire
        post_data = {
            'action[start_questionnaire]': 'Start Questionnaire'
        }
        resp = self.client.post('/questionnaire/0/789/introduction',
                                data=post_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)

        block_one_url = resp.headers['Location']

        resp = self.client.get(block_one_url, follow_redirects=False)
        self.assertEquals(resp.status_code, 200)

        # We are in the Questionnaire
        content = resp.get_data(True)
        self.assertRegexpMatches(content,
                                 'Theme selected: Star Wars')
