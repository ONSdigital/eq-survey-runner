from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.mci import mci_test_urls


class TestClearValue(IntegrationTestCase):
    """
    Issue 383 says that when a valid answer which has previously passed validation is replaced by one an invalid answer
    the invalid answer is not re-displayed to the user, but the previously validated one is.
    This test runs that scenario and verifies that the application correctly re-displays the invalid value
    """
    def test_clear_value(self):
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
        # check with have some guidance
        self.assertRegexpMatches(content, "alcoholic drink")

        # We fill in our answers using an incorrect date range
        # This is to ensure that our valid retail total gets stored
        # but that we do not proceed to the next page
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
            "e81adc6d-6fb0-4155-969c-d0d646f15345": "100000",   # Valid value
            # User Action
            "action[save_continue]": "Save &amp; Continue"
        }

        # We submit the form
        resp = self.client.post(block_one_url, data=form_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 200)

        # Get the page content
        content = resp.get_data(True)
        self.assertRegexpMatches(content, "The &#39;period to&#39; date cannot be before the &#39;period from&#39; date.")

        # Fill the dates incorrectly again, but this time supply an invalid value for retail total
        form_data = {
            # Start Date
            "6fd644b0-798e-4a58-a393-a438b32fe637-day": "30",
            "6fd644b0-798e-4a58-a393-a438b32fe637-month": "04",
            "6fd644b0-798e-4a58-a393-a438b32fe637-year": "2016",
            # End Date
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-day": "01",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-month": "04",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-year": "2016",
            # Total Turnover
            "e81adc6d-6fb0-4155-969c-d0d646f15345": "Invalid Retail Total",
            # User action
            "action[save_continue]": "Save &amp; Continue"
        }

        # We submit the form
        resp = self.client.post(block_one_url, data=form_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 200)

        # Get the page content again
        content = resp.get_data(True)
        self.assertRegexpMatches(content, "The &#39;period to&#39; date cannot be before the &#39;period from&#39; date.")
        self.assertRegexpMatches(content, "Please only enter whole numbers into the field.")
        self.assertNotRegex(content, '100000')  # We have cleared the valid value
        self.assertRegexpMatches(content, 'Invalid Retail Total')  # Our invalid value is redisplayed

        # Fill the dates incorrectly again, but this time supply an valid value for retail total
        form_data = {
            # Start Date
            "6fd644b0-798e-4a58-a393-a438b32fe637-day": "30",
            "6fd644b0-798e-4a58-a393-a438b32fe637-month": "04",
            "6fd644b0-798e-4a58-a393-a438b32fe637-year": "2016",
            # End Date
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-day": "01",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-month": "04",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-year": "2016",
            # Total Turnover
            "e81adc6d-6fb0-4155-969c-d0d646f15345": "1000",
            # User action
            "action[save_continue]": "Save &amp; Continue"
        }

        # We submit the form
        resp = self.client.post(block_one_url, data=form_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 200)

        # Get the page content again
        content = resp.get_data(True)
        self.assertRegexpMatches(content, "The &#39;period to&#39; date cannot be before the &#39;period from&#39; date.")
        self.assertNotRegex(content, "Please only enter whole numbers into the field.")  # Our message has gone
        self.assertNotRegex(content, 'Invalid Retail Total')  # Our invalid value has gone
        self.assertRegexpMatches(content, '1000')  # Our new valid value is redisplayed
