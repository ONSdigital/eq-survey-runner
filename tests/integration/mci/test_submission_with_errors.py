from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.mci import mci_test_urls


class TestSubmissionWithErrors(IntegrationTestCase):

    def test_submission_with_errors(self):
        # Get a token
        token = create_token('0205', '1')
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

        block_one_url = resp.headers['Location']

        resp = self.client.get(block_one_url, follow_redirects=False)
        self.assertEquals(resp.status_code, 200)

        # We are in the Questionnaire
        content = resp.get_data(True)
        self.assertRegexpMatches(content, '<title>Survey</title>')
        self.assertRegexpMatches(content, '>Monthly Business Survey - Retail Sales Index</')
        self.assertRegexpMatches(content, "What are the dates of the sales period you are reporting for\?")
        self.assertRegexpMatches(content, ">Save and continue<")

        form_data = {
              # Start Date
              "6fd644b0-798e-4a58-a393-a438b32fe637-day": "01",
              "6fd644b0-798e-4a58-a393-a438b32fe637-month": "4",
              "6fd644b0-798e-4a58-a393-a438b32fe637-year": "2016",
              # End Date
              "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-day": "30",
              "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-month": "04",
              "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-year": "2016",
              # Total Turnover
              "e81adc6d-6fb0-4155-969c-d0d646f15345": "abc",
              # User Action
              "action[save_continue]": "Save &amp; Continue"
          }

        resp = self.client.post(block_one_url, data=form_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 200)

        # We submit our answers
        post_data = {
            "action[submit_answers]": "Submit answers"
        }
        resp = self.client.post(mci_test_urls.MCI_0205_SUBMIT, data=post_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)
        self.assertRegexpMatches(resp.headers['Location'], block_one_url)
        resp = self.client.get(resp.headers['Location'], follow_redirects=True)
        self.assertEquals(resp.status_code, 200)
