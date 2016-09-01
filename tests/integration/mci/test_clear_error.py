from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase


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
        self.assertEquals(resp.status_code, 200)

        # We are on the landing page
        content = resp.get_data(True)

        self.assertRegexpMatches(content, '<title>Introduction</title>')
        self.assertRegexpMatches(content, '>Get Started<')
        self.assertRegexpMatches(content, '(?s)Monthly Business Survey - Retail Sales Index.*?Monthly Business Survey - Retail Sales Index')

        # We proceed to the questionnaire
        post_data = {
            'action[start_questionnaire]': 'Start Questionnaire'
        }
        resp = self.client.post('/questionnaire/1/0205/201604/789/introduction', data=post_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)

        block_one_url = resp.headers['Location']

        resp = self.client.get(block_one_url, follow_redirects=False)
        self.assertEquals(resp.status_code, 200)

        # We are in the Questionnaire
        content = resp.get_data(True)
        self.assertRegexpMatches(content, '<title>Survey</title>')
        self.assertRegexpMatches(content, '>Monthly Business Survey - Retail Sales Index</')
        self.assertRegexpMatches(content, "What are the dates of the sales period you are reporting for\?")
        self.assertRegexpMatches(content, ">Save &amp; Continue<")
        # check with have some guidance
        self.assertRegexpMatches(content, "alcoholic drink")

        # We fill in our answers using an incorrect date range
        form_data = {
            # Start Date
            "6fd644b0-798e-4a58-a393-a438b32fe637-day": "30",
            "6fd644b0-798e-4a58-a393-a438b32fe637-month": "4",
            "6fd644b0-798e-4a58-a393-a438b32fe637-year": "2016",
            # End Date
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-day": "01",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-month": "04",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-year": "2016",
            # Total Turnover
            "e81adc6d-6fb0-4155-969c-d0d646f15345": "100000",
            # User Action
            "action[save_continue]": "Save &amp; Continue"
        }

        # We submit the form
        resp = self.client.post(block_one_url, data=form_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)

        # We are back on the page with validation errors
        self.assertRegexpMatches(resp.headers['Location'], block_one_url)

        # Follow the redirect back
        resp = self.client.get(block_one_url, follow_redirects=False)
        self.assertEquals(resp.status_code, 200)

        # Get the page content
        content = resp.get_data(True)
        self.assertRegexpMatches(content, "The &#39;to&#39; date cannot be before the &#39;from&#39; date.")

        # Fill the dates in correctly, but this time miss out the required value
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
            "e81adc6d-6fb0-4155-969c-d0d646f15345": "",
            # User action
            "action[save_continue]": "Save &amp; Continue"
        }

        # We submit the form
        resp = self.client.post(block_one_url, data=form_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)

        # We are back on the page with validation errors
        self.assertRegexpMatches(resp.headers['Location'], block_one_url)

        # Follow the redirect back
        resp = self.client.get(block_one_url, follow_redirects=False)
        self.assertEquals(resp.status_code, 200)

        # Get the page content again
        content = resp.get_data(True)
        self.assertRegexpMatches(content, "Please provide a value, even if your value is 0.")
        self.assertNotRegex(content, "The &#39;to&#39; date cannot be before the &#39;from&#39; date.")
