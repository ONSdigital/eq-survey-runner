from tests.integration.mci import mci_test_urls
from tests.integration.integration_test_case import IntegrationTestCase


class TestSubmissionWithErrors(IntegrationTestCase):

    def test_submission_with_errors(self):
        self.launchSurvey('1', '0205')

        # We are on the landing page
        self.assertInPage('>Start survey<')
        self.assertInPage('Monthly Business Survey - Retail Sales Index')

        # We proceed to the questionnaire
        self.post(action='start_questionnaire')

        # We are in the Questionnaire
        self.assertInPage('>Monthly Business Survey - Retail Sales Index</')
        self.assertInPage("What are the dates of the sales period you are reporting for?")
        self.assertInPage(">Save and continue<")

        form_data = {
            # Start Date
            'empire-strikes-back-from-answer-day': '01',
            'empire-strikes-back-from-answer-month': '4',
            'empire-strikes-back-from-answer-year': '2016',
            # End Date
            'empire-strikes-back-to-answer-day': '30',
            'empire-strikes-back-to-answer-month': '4',
            'empire-strikes-back-to-answer-year': '2016'
        }

        self.post(form_data)
        self.assertInUrl('reporting-period')
        self.assertInPage('This page has 3 errors')

        # We try to submit our answers; we'll be re-directed back
        self.post(url=mci_test_urls.MCI_0205_SUMMARY, action=None)
        self.assertInUrl('reporting-period')
        self.assertNotInPage('This page has 3 errors')
