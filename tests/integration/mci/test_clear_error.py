from app.validation.error_messages import error_messages
from tests.integration.integration_test_case import IntegrationTestCase


class TestClearError(IntegrationTestCase):
    """
    Issue 374 says that when a date range fails validation and is corrected, the error message is displayed
    again if another item on the form fails validation despite the date range being correct.  This test explores
    that functionality and proves that the issue has been resolved.
    """
    def test_clear_error(self):
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
        self.assertInBody(str(error_messages['INVALID_DATE_RANGE']))

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
        self.assertInBody('Enter an answer to continue.')
        self.assertNotInBody(str(error_messages['INVALID_DATE_RANGE']))
