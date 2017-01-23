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
        self.assertEqual(resp.status_code, 200)

        # We are on the landing page
        content = resp.get_data(True)

        self.assertRegex(content, '<title>Introduction</title>', content)
        self.assertRegex(content, '>Start survey<', content)
        self.assertRegex(content, 'Monthly Business Survey - Retail Sales Index', content)

        # We proceed to the questionnaire
        post_data = {
            'action[start_questionnaire]': 'Start Questionnaire'
        }
        resp = self.client.post(mci_test_urls.MCI_0205_INTRODUCTION, data=post_data, follow_redirects=False)
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
        # check with have some guidance
        self.assertIn("alcoholic drink", content)

        # We fill in our answers using an incorrect date range
        # This is to ensure that our valid retail total gets stored
        # but that we do not proceed to the next page
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
            "total-retail-turnover": "100000",   # Valid value
            # User Action
            "action[save_continue]": "Save &amp; Continue"
        }

        # We submit the form
        resp = self.client.post(block_one_url, data=form_data, follow_redirects=False)
        self.assertEqual(resp.status_code, 200)

        # Get the page content
        content = resp.get_data(True)
        self.assertIn("The &#39;period to&#39; date cannot be before the &#39;period from&#39; date.", content)

        # Fill the dates incorrectly again, but this time supply an invalid value for retail total
        form_data = {
            # Start Date
            "period-from-day": "30",
            "period-from-month": "04",
            "period-from-year": "2016",
            # End Date
            "period-to-day": "01",
            "period-to-month": "04",
            "period-to-year": "2016",
            # Total Turnover
            "total-retail-turnover": "Invalid Retail Total",
            # User action
            "action[save_continue]": "Save &amp; Continue"
        }

        # We submit the form
        resp = self.client.post(block_one_url, data=form_data, follow_redirects=False)
        self.assertEqual(resp.status_code, 200)

        # Get the page content again
        content = resp.get_data(True)
        self.assertIn("The &#39;period to&#39; date cannot be before the &#39;period from&#39; date.", content)
        self.assertIn("Please only enter whole numbers into the field.", content)
        self.assertNotRegex(content, '100000', content)  # We have cleared the valid value
        self.assertIn('Invalid Retail Total', content)  # Our invalid value is redisplayed

        # Fill the dates incorrectly again, but this time supply an valid value for retail total
        form_data = {
            # Start Date
            "period-from-day": "30",
            "period-from-month": "04",
            "period-from-year": "2016",
            # End Date
            "period-to-day": "01",
            "period-to-month": "04",
            "period-to-year": "2016",
            # Total Turnover
            "total-retail-turnover": "1000",
            # User action
            "action[save_continue]": "Save &amp; Continue"
        }

        # We submit the form
        resp = self.client.post(block_one_url, data=form_data, follow_redirects=False)
        self.assertEqual(resp.status_code, 200)

        # Get the page content again
        content = resp.get_data(True)
        self.assertIn("The &#39;period to&#39; date cannot be before the &#39;period from&#39; date.", content)
        self.assertNotRegex(content, "Please only enter whole numbers into the field.", content)  # Our message has gone
        self.assertNotRegex(content, 'Invalid Retail Total', content)  # Our invalid value has gone
        self.assertIn('1000', content)  # Our new valid value is redisplayed
