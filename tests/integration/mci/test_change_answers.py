from tests.integration.integration_test_case import IntegrationTestCase


class TestHappyPath(IntegrationTestCase):

    def test_happy_path_203(self):
        self.happy_path('1', '0203')

    def test_happy_path_205(self):
        self.happy_path('1', '0205')

    def happy_path(self, eq_id, form_type_id):
        self.launchSurvey(eq_id, form_type_id)

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
            'total-retail-turnover': '100000'
        }

        # We submit the form
        self.post(form_data)

        # There are no validation errors (we're on the summary screen)
        self.assertInUrl('summary')
        self.assertInPage('>Monthly Business Survey - Retail Sales Index</')
        self.assertInPage('>Your responses<')
        self.assertInPage('Please check carefully before submission')
        self.assertInPage('>Submit answers<')
