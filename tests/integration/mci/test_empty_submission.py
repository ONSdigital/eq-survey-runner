from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.mci import mci_test_urls


class TestEmptySubmission(IntegrationTestCase):

    def test_empty_submission_205(self):
        self.empty_submission('0205', '1')

    def empty_submission(self, form_type_id, eq_id):
        # Get a token
        token = create_token(form_type_id, eq_id)
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=True)
        self.assertEquals(resp.status_code, 200)

        # We are on the landing page
        content = resp.get_data(True)
        self.assertRegexpMatches(content, '<title>Introduction</title>')
        self.assertRegexpMatches(content, '>Start survey<')
        self.assertRegexpMatches(content, 'Monthly Business Survey - Retail Sales Index')

        # We proceed to the questionnaire
        post_data = {
            'action[start_questionnaire]': 'Start Questionnaire'
        }
        resp = self.client.post(mci_test_urls.MCI_0205_INTRODUCTION, data=post_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)

        # We proceed to the questionnaire
        resp = self.client.get(mci_test_urls.MCI_0205_BLOCK1, follow_redirects=True)
        self.assertEquals(resp.status_code, 200)

        # We are in the Questionnaire
        content = resp.get_data(True)
        self.assertRegexpMatches(content, "What are the dates of the sales period you are reporting for\?")
        self.assertRegexpMatches(content, ">Save and continue<")

        form_data = {
            # Start Date
            "6fd644b0-798e-4a58-a393-a438b32fe637-day": "",
            "6fd644b0-798e-4a58-a393-a438b32fe637-month": "",
            "6fd644b0-798e-4a58-a393-a438b32fe637-year": "",
            # End Date
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-day": "",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-month": "",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-year": "",
            # Total Turnover
            "e81adc6d-6fb0-4155-969c-d0d646f15345": "",
            # User action
            "action[save_continue]": "Save &amp; continue"
        }

        # We submit the form without data
        resp = self.client.post(mci_test_urls.MCI_0205_BLOCK1, data=form_data, follow_redirects=True)
        self.assertEquals(resp.status_code, 200)
        content = resp.get_data(True)
        self.assertRegexpMatches(content, "Please provide an answer to continue.")
        self.assertRegexpMatches(content, "Please provide a value, even if your value is 0.")

        # We try to access the submission page without correction
        resp = self.client.get(mci_test_urls.MCI_0205_SUMMARY, follow_redirects=True)
        self.assertEquals(resp.status_code, 200)
        content = resp.get_data(True)
        self.assertRegexpMatches(content, "What are the dates of the sales period you are reporting for\?")

        form_data = {
            # Start Date
            "6fd644b0-798e-4a58-a393-a438b32fe637-day": "01",
            "6fd644b0-798e-4a58-a393-a438b32fe637-month": "04",
            "6fd644b0-798e-4a58-a393-a438b32fe637-year": "2016",
            # End Date
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-day": "30",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-month": "04",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-year": "2016",
            # Total Turnover
            "e81adc6d-6fb0-4155-969c-d0d646f15345": "100000",
            # User action
            "action[save_continue]": "Save &amp; continue"
        }

        # We correct our answers and submit
        resp = self.client.post(mci_test_urls.MCI_0205_BLOCK1, data=form_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)

        # There are no validation errors
        self.assertRegexpMatches(resp.headers['Location'], mci_test_urls.MCI_0205_SUMMARY_REGEX)
        resp = self.client.get(resp.headers['Location'], follow_redirects=True)
        self.assertEquals(resp.status_code, 200)

        # We are on the review answers page
        content = resp.get_data(True)
        self.assertRegexpMatches(content, '>Your responses<')
        self.assertRegexpMatches(content, 'Please check carefully before submission')
        self.assertRegexpMatches(content, '>Submit answers<')

        # We submit our answers
        post_data = {
            'action[submit_answers]': "Submit Answers"
        }
        resp = self.client.post(mci_test_urls.MCI_0205_SUMMARY, data=post_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)
        self.assertRegexpMatches(resp.headers['Location'], mci_test_urls.MCI_0205_THANKYOU_REGEX)
        resp = self.client.get(resp.headers['Location'], follow_redirects=True)
        self.assertEquals(resp.status_code, 200)

        # We are on the thank you page
        content = resp.get_data(True)
        self.assertRegexpMatches(content, '<title>Submission Successful</title>')
