from tests.integration.integration_test_case import IntegrationTestCase


class TestClearValue(IntegrationTestCase):
    """
    Issue 383 says that when a valid answer which has previously passed validation is replaced by one an invalid answer
    the invalid answer is not re-displayed to the user, but the previously validated one is.
    This test runs that scenario and verifies that the application correctly re-displays the invalid value
    """
    def test_clear_value(self):
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
        # This is to ensure that our valid retail total gets stored
        # but that we do not proceed to the next page
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
            'total-retail-turnover': '100000'  # Valid value
        }

        # We submit the form
        self.post(form_data)
        self.assertInPage('The &#39;period to&#39; date cannot be before the &#39;period from&#39; date.')

        # Fill the dates incorrectly again, but this time supply an invalid value for retail total
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
            'total-retail-turnover': 'Invalid Retail Total'
        }

        # We submit the form
        self.post(form_data)

        # Get the page content again
        self.assertInPage('The &#39;period to&#39; date cannot be before the &#39;period from&#39; date.')
        self.assertInPage('Please only enter whole numbers into the field.')
        self.assertNotInPage('100000')  # We have cleared the valid value
        self.assertInPage('Invalid Retail Total')  # Our invalid value is redisplayed

        # Fill the dates incorrectly again, but this time supply an valid value for retail total
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
            'total-retail-turnover': '1000'
        }

        # We submit the form
        self.post(form_data)

        self.assertInPage('The &#39;period to&#39; date cannot be before the &#39;period from&#39; date.')
        self.assertNotInPage('Please only enter whole numbers into the field.')  # Our message has gone
        self.assertNotInPage('Invalid Retail Total')  # Our invalid value has gone
        self.assertInPage('1000')  # Our new valid value is redisplayed
