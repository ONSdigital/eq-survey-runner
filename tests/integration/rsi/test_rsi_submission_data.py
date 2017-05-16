from tests.integration.integration_test_case import IntegrationTestCase


class TestRsiSubmissionData(IntegrationTestCase):

    def test_submission_data_1_0102(self):
        self.launchSurvey('1', '0102', roles=['dumper'])

        # We are on the landing page
        self.assertInPage('>Start survey<')
        self.assertInPage('Monthly Business Survey - Retail Sales Index')

        # We proceed to the questionnaire
        self.post(action='start_questionnaire')

        # We are in the Questionnaire
        self.assertInPage('>Monthly Business Survey - Retail Sales Index</')
        self.assertInPage('What are the dates of the period that you will be reporting for?')
        self.assertInPage('>Save and continue<')

        # When I submit an answer
        form_data = {
            # Start Date
            'period-from-day': '01',
            'period-from-month': '4',
            'period-from-year': '2016',
            # End Date
            'period-to-day': '30',
            'period-to-month': '4',
            'period-to-year': '2016',
        }
        # We submit the form
        self.post(form_data)
        self.post(post_data={'total-retail-turnover-answer': '100'})
        self.post(post_data={'internet-sales-answer': '50'})
        self.post(post_data={'changes-in-retail-turnover-answer': 'Down streams data test'})

        # There are no validation errors (we're on the summary screen)
        self.assertInUrl('summary')
        self.assertInPage('>Monthly Business Survey - Retail Sales Index</')
        self.assertInPage('>Your responses<')
        self.assertInPage('Please check your responses carefully before submitting')
        self.assertInPage('>Submit answers<')

        # And the JSON response contains the data I submitted
        actual = self.dumpSubmission()

        expected = {
            "submission": {
                "version": "0.0.1",
                "submitted_at": actual['submission']['submitted_at'],
                "tx_id": actual['submission']['tx_id'],
                "type": "uk.gov.ons.edc.eq:surveyresponse",
                "collection": {
                    "instrument_id": "0102",
                    "period": "201604",
                    "exercise_sid": "789"
                },
                "survey_id": "023",
                "flushed": False,
                "origin": "uk.gov.ons.edc.eq",
                "metadata": {
                    "user_id": "integration-test",
                    "ru_ref": "123456789012A"
                },
                "data": {
                    "11": "01/04/2016",
                    "12": "30/04/2016",
                    "20": "100",
                    "21": "50",
                    "146": "Down streams data test"
                }
            }
        }

        # Enable full dictionary diffs on test failure
        self.maxDiff = None
        self.assertDictEqual(actual, expected)

    def test_submission_data_1_0112(self):
        self.launchSurvey('1', '0112', roles=['dumper'])

        # We are on the landing page
        self.assertInPage('>Start survey<')
        self.assertInPage('Monthly Business Survey - Retail Sales Index')

        # We proceed to the questionnaire
        self.post(action='start_questionnaire')

        # We are in the Questionnaire
        self.assertInPage('>Monthly Business Survey - Retail Sales Index</')
        self.assertInPage('What are the dates of the period that you will be reporting for?')
        self.assertInPage('>Save and continue<')

        # When I submit an answer
        form_data = {
            # Start Date
            'period-from-day': '01',
            'period-from-month': '4',
            'period-from-year': '2016',
            # End Date
            'period-to-day': '30',
            'period-to-month': '4',
            'period-to-year': '2016',
        }

        # We submit the form
        self.post(form_data)
        self.post(post_data={'total-retail-turnover-answer': '100'})
        self.post(post_data={'internet-sales-answer': '50'})
        self.post(post_data={'changes-in-retail-turnover-answer': 'Down streams data test'})

        form_data = {
            'male-employees-over-30-hours': '1',
            'male-employees-under-30-hours': '2',
            'female-employees-over-30-hours': '3',
            'female-employees-under-30-hours': '4',
            'total-number-employees': '5',
        }
        self.post(form_data)

        self.post(post_data={'changes-in-employees-answer': 'change in number of employees'})

        # There are no validation errors (we're on the summary screen)
        self.assertInUrl('summary')
        self.assertInPage('>Monthly Business Survey - Retail Sales Index</')
        self.assertInPage('>Your responses<')
        self.assertInPage('Please check your responses carefully before submitting')
        self.assertInPage('>Submit answers<')

        # And the JSON response contains the data I submitted
        actual = self.dumpSubmission()

        expected = {
            "submission": {
                "type": "uk.gov.ons.edc.eq:surveyresponse",
                "submitted_at": actual['submission']['submitted_at'],
                "version": "0.0.1",
                "survey_id": "023",
                "flushed": False,
                "data": {
                    "11": "01/04/2016",
                    "12": "30/04/2016",
                    "20": "100",
                    "21": "50",
                    "50": "5",
                    "51": "1",
                    "52": "2",
                    "53": "3",
                    "54": "4",
                    "146": "Down streams data test",
                    "147": "change in number of employees"
                },
                "collection": {
                    "exercise_sid": "789",
                    "instrument_id": "0112",
                    "period": "201604"
                },
                "origin": "uk.gov.ons.edc.eq",
                "metadata": {
                    "ru_ref": "123456789012A",
                    "user_id": "integration-test"
                },
                "tx_id": actual['submission']['tx_id']
            }
        }

        # Enable full dictionary diffs on test failure
        self.maxDiff = None
        self.assertDictEqual(actual, expected)
