from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.mci import mci_test_urls


class TestEmptyComments(IntegrationTestCase):

    def test_empty_comments(self):
        self.launchSurvey('1', '0203')

        # We are on the landing page
        self.assertInPage('>Start survey<')
        self.assertInPage('Monthly Business Survey - Retail Sales Index')

        # We proceed to the questionnaire
        self.post(action='start_questionnaire')

        # We are in the Questionnaire
        self.assertInPage('>Monthly Business Survey - Retail Sales Index</')
        self.assertInPage('What are the dates of the sales period you are reporting for?')
        self.assertInPage('>Save and continue<')

        # We fill in our answers
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
            'total-retail-turnover': '100000',
            # Empty comment
            'reason-for-change': '  '
        }

        # We submit the form
        self.post(form_data)

        # There are no validation errors
        self.assertInUrl(mci_test_urls.MCI_0203_SUMMARY)

        # We are on the review answers page
        self.assertInPage('>Monthly Business Survey - Retail Sales Index</')
        self.assertInPage('>Your responses<')
        self.assertInPage('Please check your responses carefully before submitting')
        self.assertInPage('>Submit answers<')

        # We submit our answers
        self.post(action=None)

        # We are on the thank you page
        self.assertRegexPage('(?s)Monthly Business Survey - Retail Sales Index.*?Monthly Business Survey - Retail Sales Index')
