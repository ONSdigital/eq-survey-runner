from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase


class TestHappyPath(IntegrationTestCase):

    def test_try_date_203(self):
        self.try_date('0203', '1')

    def test_try_another_data_203(self):
        self.try_another_date('0203', '1')

    def test_try_date_205(self):
        self.try_date('0205', '1')

    def test_try_another_date_205(self):
        self.try_another_date('0205', '1')

    def try_date(self, form_type_id, eq_id):
        # Get a token
        start_date = "2016-04-01"
        end_date = "2016-04-30"

        token = create_token(form_type_id, eq_id, start_date, end_date)
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=True)
        self.assertEquals(resp.status_code, 200)

        # We are on the landing page
        content = resp.get_data(True)

        self.assertRegexpMatches(content, '<title>Introduction</title>')

        # We proceed to the questionnaire
        post_data = {
            'action[start_questionnaire]': 'Start Questionnaire'
        }
        resp = self.client.post('/questionnaire/' + eq_id + '/' + form_type_id + '/789/introduction', data=post_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)

        block_one_url = resp.headers['Location']

        resp = self.client.get(block_one_url, follow_redirects=False)
        self.assertEquals(resp.status_code, 200)

        # We are in the Questionnaire
        content = resp.get_data(True)
        self.assertRegexpMatches(content, '<title>Survey</title>')
        self.assertRegexpMatches(content, '>Monthly Business Survey - Retail Sales Index</')
        self.assertRegexpMatches(content, "What are the dates of the sales period you are reporting for\?")
        self.assertRegexpMatches(content, "1 April 2016")
        self.assertRegexpMatches(content, "30 April 2016")

    def try_another_date(self, form_type_id, eq_id):
        # Try another date
        # Get a token
        token = create_token(form_type_id, eq_id, '2017-08-01', '2017-08-31')
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=True)
        self.assertEquals(resp.status_code, 200)

        # We are on the landing page
        content = resp.get_data(True)

        self.assertRegexpMatches(content, '<title>Introduction</title>')

        # We proceed to the questionnaire
        post_data = {
            'action[start_questionnaire]': 'Start Questionnaire'
        }
        resp = self.client.post('/questionnaire/' + eq_id + '/' + form_type_id + '/789/introduction', data=post_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)

        block_one_url = resp.headers['Location']

        resp = self.client.get(block_one_url, follow_redirects=False)
        self.assertEquals(resp.status_code, 200)

        # We are in the Questionnaire
        content = resp.get_data(True)
        self.assertRegexpMatches(content, '<title>Survey</title>')
        self.assertRegexpMatches(content, '>Monthly Business Survey - Retail Sales Index</')
        self.assertRegexpMatches(content, "What are the dates of the sales period you are reporting for\?")
        self.assertRegexpMatches(content, "1 August 2017")
        self.assertRegexpMatches(content, "31 August 2017")
