
from tests.integration.integration_test_case import IntegrationTestCase


class TestCensusCommunalSubmissionData(IntegrationTestCase):

    def test_census_communal_data_matches_census_communal(self):
        self.complete_survey('census', 'communal')

        # Only verifying 'data'
        actual_downstream_data = self.dumpSubmission()['submission']['data']
        expected_downstream_data = self.get_expected_submission_data()

        self.assertCountEqual(actual_downstream_data, expected_downstream_data)

    @staticmethod
    def get_expected_submission_data():
        expected_downstream_data = [
            {
                "value": "Hotel",
                "group_id": "communal-establishment",
                "answer_id": "establishment-type-answer",
                "block_id": "establishment-type",
                "answer_instance": 0,
                "group_instance": 0
            },
            {
                "value": "",
                "group_id": "communal-establishment",
                "answer_id": "establishment-type-answer-other",
                "block_id": "establishment-type",
                "answer_instance": 0,
                "group_instance": 0
            },
            {
                "value": 20,
                "group_id": "communal-establishment",
                "answer_id": "bed-spaces-answer",
                "block_id": "bed-spaces",
                "answer_instance": 0,
                "group_instance": 0
            },
            {
                "value": "Yes",
                "group_id": "communal-establishment",
                "answer_id": "usual-residents-answer",
                "block_id": "usual-residents",
                "answer_instance": 0,
                "group_instance": 0
            },
            {
                "value": 99,
                "group_id": "communal-establishment",
                "answer_id": "usual-residents-number-answer",
                "block_id": "usual-residents-number",
                "answer_instance": 0,
                "group_instance": 0
            },
            {
                "value": [
                    "Family Members",
                    "Paying Guests",
                    "Staff",
                    "Other"
                ],
                "group_id": "communal-establishment",
                "answer_id": "describe-residents-answer",
                "block_id": "describe-residents",
                "answer_instance": 0,
                "group_instance": 0
            },
            {
                "value": "Sports visitors",
                "group_id": "communal-establishment",
                "answer_id": "describe-residents-answer-other",
                "block_id": "describe-residents",
                "answer_instance": 0,
                "group_instance": 0
            },
            {
                "value": "Online",
                "group_id": "communal-establishment",
                "answer_id": "completion-preference-individual-answer",
                "block_id": "completion-preference-individual",
                "answer_instance": 0,
                "group_instance": 0
            },
            {
                "value": "Online",
                "group_id": "communal-establishment",
                "answer_id": "completion-preference-establishment-answer",
                "block_id": "completion-preference-establishment",
                "answer_instance": 0,
                "group_instance": 0
            },
            {
                "value": "Yes",
                "group_id": "communal-establishment",
                "answer_id": "further-contact-answer",
                "block_id": "further-contact",
                "answer_instance": 0,
                "group_instance": 0
            },
            {
                "value": "0123456789",
                "group_id": "communal-establishment",
                "answer_id": "contact-details-answer-phone",
                "block_id": "contact-details",
                "answer_instance": 0,
                "group_instance": 0
            },
            {
                "value": "danny.boje@gmail.com",
                "group_id": "communal-establishment",
                "answer_id": "contact-details-answer-email",
                "block_id": "contact-details",
                "answer_instance": 0,
                "group_instance": 0
            },
            {
                "value": "Danny",
                "group_id": "communal-establishment",
                "answer_id": "contact-details-answer-name",
                "block_id": "contact-details",
                "answer_instance": 0,
                "group_instance": 0
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
