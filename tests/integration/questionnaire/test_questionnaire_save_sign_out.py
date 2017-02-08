from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase


class TestSaveSignOut(IntegrationTestCase):

    def test_save_sign_out_with_mandatory_question_not_answered(self):
        # We can save and go to the sign-out page without having to fill in mandatory answer
        base_url = '/questionnaire/1/0205/789/'

        # Given
        token = create_token('0205', '1')
        self.client.get('/session?token=' + token.decode(), follow_redirects=False)

        # When
        post_data = {
            'action[start_questionnaire]': 'Start Questionnaire'
        }
        resp = self.client.post(base_url + 'introduction', data=post_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)

        block_one_url = resp.headers['Location']

        post_data = {
            "total-retail-turnover": "1000",
            "action[save_sign_out]": "Save and sign out"
        }
        resp = self.client.post(block_one_url, data=post_data, follow_redirects=False)

        self.assertEquals(resp.status_code, 302)

        # Then
        # we are presented with the sign out page
        self.assertTrue("signed-out" in resp.headers['Location'])

        resp = self.client.get(resp.headers['Location'], follow_redirects=False)
        self.assertEquals(resp.status_code, 200)

    def test_save_sign_out_with_non_mandatory_validation_error(self):
        # We can't save if a validation error is caused, this doesn't include missing a mandatory question
        base_url = '/questionnaire/1/0205/789/'

        # Given
        token = create_token('0205', '1')
        self.client.get('/session?token=' + token.decode(), follow_redirects=False)

        # When
        post_data = {
            'action[start_questionnaire]': 'Start Questionnaire'
        }
        resp = self.client.post(base_url + 'introduction', data=post_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)

        block_one_url = resp.headers['Location']

        post_data = {
            "total-retail-turnover": "error",
            "action[save_sign_out]": "Save and sign out"
        }
        resp = self.client.post(block_one_url, data=post_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 200)
        # Then
        # we are presented with an error message
        content = resp.get_data(True)
        self.assertRegexpMatches(content, 'Please only enter whole numbers into the field.')

    def test_save_sign_out_complete_a_block_then_revisit_it(self):

        # If a user completes a block, but then goes back and uses save and come back on that block, that block
        # should no longer be considered complete and on re-authenticate it should return to it

        base_url = '/questionnaire/1/0102/789/'

        token = create_token('0102', '1')
        self.client.get('/session?token=' + token.decode(), follow_redirects=False)

        post_data = {
            'action[start_questionnaire]': 'Start Questionnaire'
        }
        resp = self.client.post(base_url + 'introduction', data=post_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)

        block_one_url = resp.headers['Location']

        post_data = {
            "period-from-day": "01",
            "period-from-month": "4",
            "period-from-year": "2016",
            "period-to-day": "30",
            "period-to-month": "4",
            "period-to-year": "2016",
            "action[save_continue]": "Save &amp; Continue"
        }

        resp = self.client.post(block_one_url, data=post_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)

        # We go back to the first page and save and complete later
        self.client.get(block_one_url, follow_redirects=False)

        post_data = {
            "action[save_sign_out]": "Save and sign out"
        }
        self.client.post(block_one_url, data=post_data, follow_redirects=False)

        # We re-authenticate and check we are on the first page
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=False)
        block_one_url = resp.headers['Location']
        self.assertRegexpMatches(block_one_url, 'reporting-period')
