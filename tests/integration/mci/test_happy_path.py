from tests.integration.integration_test_case import IntegrationTestCase


class TestHappyPath(IntegrationTestCase):

    def test_happy_path_203(self):
        self._happy_path('0203', '1')

    def test_happy_path_205(self):
        self._happy_path('0205', '1')

    def _happy_path(self, form_type_id, eq_id):
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

        # check with have some guidance
        self.assertInPage('alcoholic drink')

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
        }

        # We submit the form
        self.post(form_data)

        # There are no validation errors
        self.assertInUrl('summary')

        # We are on the review answers page
        self.assertInPage('>Monthly Business Survey - Retail Sales Index</')
        self.assertInPage('>Your responses<')
        self.assertInPage('Please check your responses carefully before submitting.')
        self.assertInPage('>Submit answers<')

        # Submit answers
        self.post(action=None)

        # We are on the thank you page
        self.assertRegexPage('(?s)Monthly Business Survey - Retail Sales Index.*?Monthly Business Survey - Retail Sales Index')
