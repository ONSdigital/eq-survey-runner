from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase


class TestHappyPath(IntegrationTestCase):

    def test_happy_path_203(self):
        self.happy_path('0203', '1')

    def test_happy_path_205(self):
        self.happy_path('0205', '1')

    def happy_path(self, form_type_id, eq_id):
        # Get a token
        token = create_token(form_type_id, eq_id)
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=True)
        self.assertEqual(resp.status_code, 200)

        # We are on the landing page
        content = resp.get_data(True)

        self.assertIn('<title>Introduction</title>', content)
        self.assertIn('>Start survey<', content)
        self.assertIn('Monthly Business Survey - Retail Sales Index', content)

        # We proceed to the questionnaire
        post_data = {
            'action[start_questionnaire]': 'Start Questionnaire'
        }
        resp = self.client.post('/questionnaire/' + eq_id + '/' + form_type_id + '/789/introduction', data=post_data, follow_redirects=False)
        self.assertEqual(resp.status_code, 302)

        block_one_url = resp.location

        resp = self.client.get(block_one_url, follow_redirects=False)
        self.assertEqual(resp.status_code, 200)

        # We are in the Questionnaire
        content = resp.get_data(True)
        self.assertIn('<title>Survey</title>', content)
        self.assertIn('>Monthly Business Survey - Retail Sales Index</', content)
        self.assertIn("What are the dates of the sales period you are reporting for?", content)
        self.assertIn(">Save and continue<", content)

        # We fill in our answers
        form_data = {
            # Start Date
            "period-from-day": "01",
            "period-from-month": "4",
            "period-from-year": "2016",
            # End Date
            "period-to-day": "30",
            "period-to-month": "04",
            "period-to-year": "2016",
            # Total Turnover
            "total-retail-turnover": "100000",
            # User Action
            "action[save_continue]": "Save &amp; Continue"
        }

        # We submit the form
        resp = self.client.post(block_one_url, data=form_data, follow_redirects=False)
        self.assertEqual(resp.status_code, 302)

        # There are no validation errors
        self.assertRegex(resp.location, r'\/questionnaire\/1/' + form_type_id + r'\/789\/summary$')

        summary_url = resp.location

        resp = self.client.get(summary_url, follow_redirects=False)
        self.assertEqual(resp.status_code, 200)

        # We are on the review answers page
        content = resp.get_data(True)
        self.assertIn('<title>Summary</title>', content)
        self.assertIn('>Monthly Business Survey - Retail Sales Index</', content)
        self.assertIn('>Your responses<', content)
        self.assertIn('Please check carefully before submission', content)
        self.assertIn('>Submit answers<', content)
