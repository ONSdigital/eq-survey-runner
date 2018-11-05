from app.validation.error_messages import error_messages
from tests.integration.integration_test_case import IntegrationTestCase


class TestClearValue(IntegrationTestCase):
    """
    Issue 383 says that when a valid answer which has previously passed validation is replaced by one an invalid answer
    the invalid answer is not re-displayed to the user, but the previously validated one is.
    This test runs that scenario and verifies that the application correctly re-displays the invalid value
    """
    def test_clear_value(self):
        self.launchSurvey('test', '0205')

        # We are on the introduction page
        self.assertInBody('>Start survey<')
        self.assertInBody('Monthly Business Survey - Retail Sales Index')

        # We proceed to the questionnaire
        self.post(action='start_questionnaire')

        # We are in the Questionnaire
        self.assertInBody('>Monthly Business Survey - Retail Sales Index</')
        self.assertInBody('What are the dates of the sales period you are reporting for?')
        self.assertInBody('>Save and continue<')

        # check with have some guidance
        self.assertInBody('alcoholic drink')

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
        self.assertInBody(str(error_messages['INVALID_DATE_RANGE']))

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
        self.assertInBody(str(error_messages['INVALID_DATE_RANGE']))
        self.assertInBody(str(error_messages['INVALID_NUMBER']))
        self.assertNotInBody('100000')  # We have cleared the valid value
        self.assertInBody('Invalid Retail Total')  # Our invalid value is redisplayed

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

        self.assertInBody(str(error_messages['INVALID_DATE_RANGE']))
        self.assertNotInBody(str(error_messages['INVALID_INTEGER'])) # Our message has gone
        self.assertNotInBody('Invalid Retail Total')  # Our invalid value has gone
        self.assertInBody('1000')  # Our new valid value is redisplayed
