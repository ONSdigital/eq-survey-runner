from tests.integration.integration_test_case import IntegrationTestCase


class TestMciSubmissionData(IntegrationTestCase):

    def test_submission_data_203(self):
        self.submission_data('1', '0203')

    def test_submission_data_205(self):
        self.submission_data('1', '0205')

    def submission_data(self, eq_id, form_type_id):
        self.launchSurvey(eq_id, form_type_id, roles=['dumper'])

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
        self.assertInPage('Please check your responses carefully before submitting')
        self.assertInPage('>Submit answers<')

        actual = self.dumpSubmission()

        expected = {
            "submission": {
                "type": "uk.gov.ons.edc.eq:surveyresponse",
                "data": {
                    "11": "01/04/2016",
                    "12": "30/04/2016",
                    "20": "100000"
                },
                "metadata": {
                    "ru_ref": "123456789012A",
                    "user_id": "integration-test"
                },
                "version": "0.0.1",
                "survey_id": "023",
                "flushed": False,
                "tx_id": actual['submission']['tx_id'],
                "submitted_at": actual['submission']['submitted_at'],
                "collection": {
                    "period": "201604",
                    "exercise_sid": "789",
                    "instrument_id": form_type_id
                },
                "origin": "uk.gov.ons.edc.eq"
            }
        }

        # Enable full dictionary diffs on test failure
        self.maxDiff = None
        self.assertDictEqual(actual, expected)
