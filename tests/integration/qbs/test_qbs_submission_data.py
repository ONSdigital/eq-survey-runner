from tests.integration.integration_test_case import IntegrationTestCase


class TestQbsSubmissionData(IntegrationTestCase):

    def test_submission_data_2_0001(self):
        self.submission_data('2', '0001')

    def submission_data(self, eq_id, form_type_id):
        self.launchSurvey(eq_id, form_type_id, roles=['dumper'])

        # We are on the landing page
        self.assertInPage('>Start survey<')
        self.assertInPage('Quarterly Business Survey')

        # We proceed to the questionnaire
        self.post(action='start_questionnaire')

        # We are in the Questionnaire
        self.assertInPage('>Quarterly Business Survey</')
        self.assertInPage('On 1 April 2016 what was the number of employees for Integration Tests?')
        self.assertInPage('>Save and continue<')

        # When I submit an answer
        self.post(post_data={'number-of-employees-male-more-30-hours': '1',
                             'number-of-employees-male-less-30-hours': '2',
                             'number-of-employees-female-more-30-hours': '3',
                             'number-of-employees-female-less-30-hours': '4',
                             'number-of-employees-total': '5'})

        # There are no validation errors (we're on the summary screen)
        self.assertInUrl('summary')
        self.assertInPage('>Quarterly Business Survey</')
        self.assertInPage('>Your responses<')
        self.assertInPage('Please check your responses carefully before submitting')
        self.assertInPage('>Submit answers<')

        # And the JSON response contains the data I submitted
        actual = self.dumpSubmission()

        expected = {
            'submission': {
                'origin': 'uk.gov.ons.edc.eq',
                'submitted_at': actual['submission']['submitted_at'],
                'collection': {
                    'exercise_sid': '789',
                    'period': '201604',
                    'instrument_id': '0001'
                    },
                'survey_id': '139',
                'flushed': False,
                'tx_id': actual['submission']['tx_id'],
                'data': {
                    '50': '5',
                    '51': '1',
                    '52': '2',
                    '53': '3',
                    '54': '4'
                },
                'type': 'uk.gov.ons.edc.eq:surveyresponse',
                'version': '0.0.1',
                'metadata': {
                    'ru_ref': '123456789012A',
                    'user_id': 'integration-test'
                }
            }
        }

        # Enable full dictionary diffs on test failure
        self.maxDiff = None
        self.assertDictEqual(actual, expected)
