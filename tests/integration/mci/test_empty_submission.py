from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.mci import mci_test_urls


class TestEmptySubmission(IntegrationTestCase):

    def test_empty_submission_205(self):
        self.empty_submission('1', '0205')

    def empty_submission(self, eq_id, form_type_id):
        self.launchSurvey(eq_id, form_type_id)

        # We are on the landing page
        self.assertInPage('>Start survey<')
        self.assertInPage('Monthly Business Survey - Retail Sales Index')

        # We proceed to the questionnaire
        self.post(action='start_questionnaire')

        # We are in the Questionnaire
        self.assertInPage('What are the dates of the sales period you are reporting for?')
        self.assertInPage('>Save and continue<')

        form_data = {
            # Start Date
            'period-from-day': '',
            'period-from-month': '',
            'period-from-year': '',
            # End Date
            'period-to-day': '',
            'period-to-month': '',
            'period-to-year': '',
            # Total Turnover
            'total-retail-turnover': ''
        }

        # We submit the form without data
        self.post(form_data)
        self.assertInPage('Please provide an answer to continue.')
        self.assertInPage('Please provide a value, even if your value is 0.')

        # We try to access the submission page without correction
        self.get(mci_test_urls.MCI_0205_SUMMARY)
        self.assertInPage('What are the dates of the sales period you are reporting for?')

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
            'total-retail-turnover': '100000'
        }

        # We correct our answers and submit
        self.post(form_data)

        # There are no validation errors
        self.assertInUrl(mci_test_urls.MCI_0205_SUMMARY)

        # We are on the review answers page
        self.assertInPage('>Your responses<')
        self.assertInPage('Please check your responses carefully before submitting')
        self.assertInPage('>Submit answers<')

        # We submit our answers
        self.post(action=None)

        # We are on the thank you page
        self.assertInUrl('thank-you')
