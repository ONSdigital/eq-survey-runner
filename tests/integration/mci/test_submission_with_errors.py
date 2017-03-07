from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.mci import mci_test_urls


class TestSubmissionWithErrors(IntegrationTestCase):

    def test_submission_with_errors(self):
        # Get a token
        token = create_token('0205', '1')
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
        resp = self.get_and_post_with_csrf_token(mci_test_urls.MCI_0205_INTRODUCTION, data=post_data, follow_redirects=False)
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

        form_data = {
            # Start Date
            "empire-strikes-back-from-answer-day": "01",
            "empire-strikes-back-from-answer-month": "4",
            "empire-strikes-back-from-answer-year": "2016",
            # End Date
            "empire-strikes-back-to-answer-day": "30",
            "empire-strikes-back-to-answer-month": "4",
            "empire-strikes-back-to-answer-year": "2016",
            # User Action
            "action[save_continue]": "Save &amp; Continue"
        }

        resp = self.get_and_post_with_csrf_token(block_one_url, data=form_data, follow_redirects=False)
        self.assertEqual(resp.status_code, 200)

        # We submit our answers
        self.get_and_post_with_csrf_token(mci_test_urls.MCI_0205_SUMMARY)
