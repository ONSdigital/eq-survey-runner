from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.mci import mci_test_urls


class TestClearError(IntegrationTestCase):
    """
    Issue 374 says that when a date range fails validation and is corrected, the error message is displayed
    again if another item on the form fails validation despite the date range being correct.  This test explores
    that functionality and proves that the issue has been resolved.
    """
    def test_clear_error(self):
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
        resp = self.client.post(mci_test_urls.MCI_0205_INTRODUCTION, data=post_data, follow_redirects=False)
        self.assertEqual(resp.status_code, 302)

        block_one_url = resp.headers['Location']

        resp = self.client.get(block_one_url, follow_redirects=False)
        self.assertEqual(resp.status_code, 200)

        # We are in the Questionnaire
        content = resp.get_data(True)
        self.assertRegex(content, '<title>Survey</title>')
        self.assertRegex(content, '>Monthly Business Survey - Retail Sales Index</')
        self.assertRegex(content, "What are the dates of the sales period you are reporting for\?")
        self.assertRegex(content, ">Save and continue<")
        # check with have some guidance
        self.assertRegex(content, "alcoholic drink")

        # We fill in our answers using an incorrect date range
        form_data = {
            # Start Date
            "period-from-day": "30",
            "period-from-month": "4",
            "period-from-year": "2016",
            # End Date
            "period-to-day": "01",
            "period-to-month": "04",
            "period-to-year": "2016",
            # Total Turnover
            "total-retail-turnover": "100000",
            # User Action
            "action[save_continue]": "Save &amp; Continue"
        }

        # We submit the form
        resp = self.client.post(block_one_url, data=form_data, follow_redirects=False)
        self.assertEqual(resp.status_code, 200)

        # Get the page content
        content = resp.get_data(True)
        self.assertRegex(content, "The &#39;period to&#39; date cannot be before the &#39;period from&#39; date.")

        # Fill the dates in correctly, but this time miss out the required value
        form_data = {
            # Start Date
            "period-from-day": "01",
            "period-from-month": "04",
            "period-from-year": "2016",
            # End Date
            "period-to-day": "30",
            "period-to-month": "04",
            "period-to-year": "2016",
            # Total Turnover
            "total-retail-turnover": "",
            # User action
            "action[save_continue]": "Save &amp; Continue"
        }

        # We submit the form
        resp = self.client.post(block_one_url, data=form_data, follow_redirects=False)
        self.assertEqual(resp.status_code, 200)

        # Get the page content again
        content = resp.get_data(True)
        self.assertRegex(content, "Please provide a value, even if your value is 0.")
        self.assertNotRegex(content, "The &#39;period to&#39; date cannot be before the &#39;period from&#39; date.")
