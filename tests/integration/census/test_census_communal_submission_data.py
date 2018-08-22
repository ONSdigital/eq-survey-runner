from mock import patch

from tests.integration.integration_test_case import IntegrationTestCase


class TestCensusCommunalSubmissionData(IntegrationTestCase):

    def test_census_communal_data_matches_census_communal(self):
        with patch('app.helpers.schema_helpers.uuid4', side_effect=range(100)):
            self.complete_survey('census', 'communal')

        # Only verifying 'data'
        actual_downstream_data = self.dumpSubmission()['submission']['data']
        expected_downstream_data = self.get_expected_submission_data()

        self.assertCountEqual(actual_downstream_data, expected_downstream_data)

    @staticmethod
    def get_expected_submission_data():
        expected_downstream_data = [
            {
                'value': 'Hotel',
                'answer_id': 'establishment-type-answer',
                'answer_instance': 0,
                'group_instance': 0,
                'group_instance_id': None,
            },
            {
                'value': '',
                'answer_id': 'establishment-type-answer-other',
                'answer_instance': 0,
                'group_instance': 0,
                'group_instance_id': None,
            },
            {
                'value': 20,
                'answer_id': 'bed-spaces-answer',
                'answer_instance': 0,
                'group_instance': 0,
                'group_instance_id': None,
            },
            {
                'value': 'Yes',
                'answer_id': 'usual-residents-answer',
                'answer_instance': 0,
                'group_instance': 0,
                'group_instance_id': None,
            },
            {
                'value': 99,
                'answer_id': 'usual-residents-number-answer',
                'answer_instance': 0,
                'group_instance': 0,
                'group_instance_id': None,
            },
            {
                'value': [
                    'Family Members',
                    'Paying Guests',
                    'Staff',
                    'Other'
                ],
                'answer_id': 'describe-residents-answer',
                'answer_instance': 0,
                'group_instance': 0,
                'group_instance_id': None,
            },
            {
                'value': 'Sports visitors',
                'answer_id': 'describe-residents-answer-other',
                'answer_instance': 0,
                'group_instance': 0,
                'group_instance_id': None,
            },
            {
                'value': 'Online',
                'answer_id': 'completion-preference-individual-answer',
                'answer_instance': 0,
                'group_instance': 0,
                'group_instance_id': None,
            },
            {
                'value': 'Online',
                'answer_id': 'completion-preference-establishment-answer',
                'answer_instance': 0,
                'group_instance': 0,
                'group_instance_id': None,
            },
            {
                'value': 'Yes',
                'answer_id': 'further-contact-answer',
                'answer_instance': 0,
                'group_instance': 0,
                'group_instance_id': None,
            },
            {
                'value': '0123456789',
                'answer_id': 'contact-details-answer-phone',
                'answer_instance': 0,
                'group_instance': 0,
                'group_instance_id': None,
            },
            {
                'value': 'danny.boje@gmail.com',
                'answer_id': 'contact-details-answer-email',
                'answer_instance': 0,
                'group_instance': 0,
                'group_instance_id': None,
            },
            {
                'value': 'Danny',
                'answer_id': 'contact-details-answer-name',
                'answer_instance': 0,
                'group_instance': 0,
                'group_instance_id': None,
            }
        ]

        return expected_downstream_data

    def complete_survey(self, eq_id, form_type_id):
        self.launchSurvey(eq_id, form_type_id, roles=['dumper'])

        # We are in the questionnaire
        self.assertInPage('Establishment')
        self.assertInPage('How would you describe your establishment?')
        self.assertInPage('>Save and continue<')

        # When I submit an answer
        self.post(post_data={'establishment-type-answer': ['Hotel']})
        self.post(post_data={'bed-spaces-answer': '20'})
        self.post(post_data={'usual-residents-answer': ['Yes']})
        self.post(post_data={'usual-residents-number-answer': '99'})

        form_data = {'describe-residents-answer': ['Family Members', 'Paying Guests', 'Staff', 'Other'],
                     'describe-residents-answer-other': 'Sports visitors'}
        self.post(form_data)
        self.post(post_data={'completion-preference-individual-answer': ['Online']})
        self.post(post_data={'completion-preference-establishment-answer': ['Online']})
        self.post(post_data={'further-contact-answer': ['Yes']})
        self.post(post_data={'contact-details-answer-name': 'Danny',
                             'contact-details-answer-email': 'danny.boje@gmail.com',
                             'contact-details-answer-phone': '0123456789'})

        # There are no validation errors (we're on the summary screen)
        self.assertInPage('You’re ready to submit your 2017 Census Test')
