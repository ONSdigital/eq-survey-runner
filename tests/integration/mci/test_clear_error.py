from tests.integration.integration_test_case import IntegrationTestCase


class TestClearError(IntegrationTestCase):
    """
    Issue 374 says that when a date range fails validation and is corrected, the error message is displayed
    again if another item on the form fails validation despite the date range being correct.  This test explores
    that functionality and proves that the issue has been resolved.
    """
    def test_clear_error(self):
        self.launchSurvey('1', '0205')

        # We are on the landing page
        self.assertInPage('>Start survey<')
        self.assertInPage('Monthly Business Survey - Retail Sales Index')

        # We proceed to the questionnaire
        self.post(action='start_questionnaire')

        # We are in the Questionnaire
        self.assertInPage('>Monthly Business Survey - Retail Sales Index</')
        self.assertInPage('What are the dates of the sales period you are reporting for?')
        self.assertInPage('>Save and continue<')

        # check with have some guidance
        self.assertInPage('alcoholic drink')

        # We fill in our answers using an incorrect date range
        form_data = {
            # Start Date
            'period-from-day': '30',
            'period-from-month': '4',
            'period-from-year': '2016',
            # End Date
            'period-to-day': '01',
            'period-to-month': '4',
            'period-to-year': '2016',
            # Total Turnover
            'total-retail-turnover': '100000'
        }

        # We submit the form
        self.post(form_data)
        self.assertInPage("The &#39;period to&#39; date cannot be before the &#39;period from&#39; date.")

        # Fill the dates in correctly, but this time miss out the required value
        form_data = {
            # Start Date
            'period-from-day': '01',
            'period-from-month': '4',
            'period-from-year': '2016',
            # End Date
            'period-to-day': '30',
            'period-to-month': '4',
            'period-to-year': '2016',
            # Total Turnover
            'total-retail-turnover': ''
        }

        # We submit the form
        self.post(form_data)

        # Check the page content again
        self.assertInPage('Please provide a value, even if your value is 0.')
        self.assertNotInPage('The &#39;period to&#39; date cannot be before the &#39;period from&#39; date.')
