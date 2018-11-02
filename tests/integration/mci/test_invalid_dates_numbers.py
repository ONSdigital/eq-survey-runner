from app.validation.error_messages import error_messages
from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.mci import mci_test_urls


class TestInvalidDateNumber(IntegrationTestCase):

    def test_correct_invalid_date(self):
        self.launchSurvey('test', '0205')

        # We are on the introduction page
        self.assertInBody('>Start survey<')
        self.assertInBody('Monthly Business Survey - Retail Sales Index')

        # We proceed to the questionnaire
        self.post(action='start_questionnaire')

        form_data = {
            # Start Date
            'period-from-day': '01',
            'period-from-month': '1',
            'period-from-year': '2016',
            # End Date
            'period-to-day': '01',
            'period-to-month': '1',
            'period-to-year': '2016',
            # Total Turnover
            'total-retail-turnover': '100000'
        }

        # We submit the form with the dates the same
        self.post(form_data)
        self.assertInBody(str(error_messages['INVALID_DATE_RANGE']))

        form_data = {
            # Start Date
            'period-from-day': '01',
            'period-from-month': '1',
            'period-from-year': '2016',
            # End Date
            'period-to-day': '01',
            'period-to-month': '1',
            'period-to-year': '2017',
            # Total Turnover
            'total-retail-turnover': '10000'
        }

        # We correct our answers and submit
        self.post(form_data)

        # There are no validation errors
        self.assertInUrl(mci_test_urls.MCI_0205_SUMMARY)

        # We are on the review answers page
        self.assertInBody('>Check your answers and submit<')
        self.assertInBody('You can check your answers below')
        self.assertInBody('>Submit answers<')

        # We submit our answers
        self.post(action=None)

        # We are on the thank you page
        self.assertInUrl('thank-you')

    def test_invalid_same_date(self):
        self.launchSurvey('test', '0205')
        self.post(action='start_questionnaire')

        form_data = {
            # Start Date
            'period-from-day': '01',
            'period-from-month': '1',
            'period-from-year': '2016',
            # End Date
            'period-to-day': '01',
            'period-to-month': '1',
            'period-to-year': '2016',
            # Total Turnover
            'total-retail-turnover': '10000'
        }

        # We submit the form with the dates the same
        self.post(form_data)
        self.assertInBody(str(error_messages['INVALID_DATE_RANGE']))

    def test_invalid_date_range(self):
        self.launchSurvey('test', '0205')
        self.post(action='start_questionnaire')

        form_data = {
            # Start Date
            'period-from-day': '01',
            'period-from-month': '1',
            'period-from-year': '2017',
            # End Date
            'period-to-day': '01',
            'period-to-month': '1',
            'period-to-year': '2016',
            # Total Turnover
            'total-retail-turnover': '10000'
        }

        # We submit the form with the front date later then the to date
        self.post(form_data)
        self.assertInBody(str(error_messages['INVALID_DATE_RANGE']))

    def test_invalid_year(self):
        self.launchSurvey('test', '0205')
        self.post(action='start_questionnaire')

        form_data = {
            # Start Date
            'period-from-day': '01',
            'period-from-month': '1',
            'period-from-year': '',
            # End Date
            'period-to-day': '01',
            'period-to-month': '1',
            'period-to-year': '',
            # Total Turnover
            'total-retail-turnover': '100000'
        }

        # We submit the form without a valid 2nd date
        self.post(form_data)
        self.assertInBody(str(error_messages['INVALID_DATE']))

    def test_invalid_integer(self):
        self.launchSurvey('test', '0205')
        self.post(action='start_questionnaire')

        form_data = {
            # Start Date
            'period-from-day': '01',
            'period-from-month': '1',
            'period-from-year': '2016',
            # End Date
            'period-to-day': '01',
            'period-to-month': '1',
            'period-to-year': '2017',
            # Total Turnover
            'total-retail-turnover': 'rubbish'
        }

        # We submit the form without a valid turnover value
        self.post(form_data)
        self.assertInBody(str(error_messages['INVALID_NUMBER']))

    def test_invalid_date_number(self):
        self.launchSurvey('test', '0205')
        self.post(action='start_questionnaire')

        form_data = {
            # Start Date
            'period-from-day': '01',
            'period-from-month': '1',
            'period-from-year': '',
            # End Date
            'period-to-day': '01',
            'period-to-month': '1',
            'period-to-year': '',
            # Total Turnover
            'total-retail-turnover': '100000'
        }

        # We submit the form with an invalid date
        self.post(form_data)
        self.assertInBody(str(error_messages['INVALID_DATE']))
