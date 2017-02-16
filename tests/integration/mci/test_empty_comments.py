from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.mci import mci_test_urls


class TestEmptyComments(IntegrationTestCase):

    def test_empty_comments(self):
        # Get a token
        token = create_token('0203', '1')
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=True)
        self.assertEqual(resp.status_code, 200)

        # We are on the landing page
        content = resp.get_data(True)

        self.assertRegex(content, '<title>Introduction</title>')
        self.assertRegex(content, '>Start survey<')
        self.assertRegex(content, 'Monthly Business Survey - Retail Sales Index')

        # We proceed to the questionnaire
        post_data = {
            'action[start_questionnaire]': 'Start Questionnaire'
        }
        resp = self.client.post(mci_test_urls.MCI_0203_INTRODUCTION, data=post_data, follow_redirects=False)
        self.assertEqual(resp.status_code, 302)

        block_one_url = resp.location

        resp = self.client.get(block_one_url, follow_redirects=False)
        self.assertEqual(resp.status_code, 200)

        # We are in the Questionnaire
        content = resp.get_data(True)
        self.assertRegex(content, '<title>Survey</title>')
        self.assertRegex(content, '>Monthly Business Survey - Retail Sales Index</')
        self.assertRegex(content, "What are the dates of the sales period you are reporting for?")
        self.assertRegex(content, ">Save and continue<")

        # We fill in our answers
        form_data = {
            # Start Date
            "period-from-day": "01",
            "period-from-month": "4",
            "period-from-year": "2016",
            # End Date
            "period-to-day": "30",
            "period-to-month": "4",
            "period-to-year": "2016",
            # Total Turnover
            "total-retail-turnover": "100000",
            # User Action
            "action[save_continue]": "Save &amp; Continue",
            # Empty comment
            "reason-for-change": "  "
        }

        # We submit the form
        resp = self.client.post(block_one_url, data=form_data, follow_redirects=False)
        self.assertEqual(resp.status_code, 302)

        # There are no validation errors
        self.assertIn(mci_test_urls.MCI_0203_SUMMARY, resp.location)

        summary_url = resp.location

        resp = self.client.get(summary_url, follow_redirects=False)
        self.assertEqual(resp.status_code, 200)

        # We are on the review answers page
        content = resp.get_data(True)
        self.assertRegex(content, '<title>Summary</title>')
        self.assertRegex(content, '>Monthly Business Survey - Retail Sales Index</')
        self.assertRegex(content, '>Your responses<')
        self.assertRegex(content, 'Please check carefully before submission')
        self.assertRegex(content, '>Submit answers<')

        # We submit our answers
        post_data = {
            "action[submit_answers]": "Submit answers"
        }
        _, resp = self.postRedirectGet('/questionnaire/1/0203/789/submit-answers', post_data)

        # We are on the thank you page
        content = resp.get_data(True)
        self.assertRegex(content, '<title>Submission Successful</title>')
        self.assertRegex(content, '(?s)Monthly Business Survey - Retail Sales Index.*?Monthly Business Survey - Retail Sales Index')
