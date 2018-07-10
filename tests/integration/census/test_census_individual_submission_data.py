from unittest.mock import patch
from tests.integration.integration_test_case import IntegrationTestCase


class TestCensusIndividualSubmissionData(IntegrationTestCase):

    def test_census_individual_data_matches_census_individual(self):
        with patch('app.questionnaire.rules._answer_is_in_repeating_group', return_value=False):
            self.complete_survey('census', 'individual')

            # Only verifying 'data'
            actual_downstream_data = self.dumpSubmission()['submission']['data']
            expected_downstream_data = self.get_expected_submission_data()

            self.assertCountEqual(actual_downstream_data, expected_downstream_data)

    @staticmethod
    def get_expected_submission_data():
        expected_downstream_data = [
            {
                'group_instance': 0,
                'value': 'Danny',
                'answer_instance': 0,
                'answer_id': 'first-name'
            },
            {
                'group_instance': 0,
                'value': 'K',
                'answer_instance': 0,
                'answer_id': 'middle-names'
            },
            {
                'group_instance': 0,
                'value': 'Boje',
                'answer_instance': 0,
                'answer_id': 'last-name'
            },
            {
                'group_instance': 0,
                'value': 'Male',
                'answer_instance': 0,
                'answer_id': 'sex-answer'
            },
            {
                'group_instance': 0,
                'value': '1988-05-12',
                'answer_instance': 0,
                'answer_id': 'date-of-birth-answer'
            },
            {
                'group_instance': 0,
                'value': 'In a registered same-sex civil partnership',
                'answer_instance': 0,
                'answer_id': 'marital-status-answer'
            },
            {
                'group_instance': 0,
                'value': 'Yes, an address within the UK',
                'answer_instance': 0,
                'answer_id': 'another-address-answer'
            },
            {
                'group_instance': 0,
                'value': '',
                'answer_instance': 0,
                'answer_id': 'another-address-answer-other'
            },
            {
                'group_instance': 0,
                'value': 'Newport',
                'answer_instance': 0,
                'answer_id': 'other-address-answer-city'
            },
            {
                'group_instance': 0,
                'value': '',
                'answer_instance': 0,
                'answer_id': 'other-address-answer-street'
            },
            {
                'group_instance': 0,
                'value': '',
                'answer_instance': 0,
                'answer_id': 'other-address-answer-county'
            },
            {
                'group_instance': 0,
                'value': '12',
                'answer_instance': 0,
                'answer_id': 'other-address-answer-building'
            },
            {
                'group_instance': 0,
                'value': 'NP10 8XG',
                'answer_instance': 0,
                'answer_id': 'other-address-answer-postcode'
            },
            {
                'group_instance': 0,
                'value': 'Friends Home',
                'answer_instance': 0,
                'answer_id': 'address-type-answer-other'
            },
            {
                'group_instance': 0,
                'value': 'Other',
                'answer_instance': 0,
                'answer_id': 'address-type-answer'
            },
            {
                'group_instance': 0,
                'value': 'Yes',
                'answer_instance': 0,
                'answer_id': 'in-education-answer'
            },
            {
                'group_instance': 0,
                'value': 'here, at this address',
                'answer_instance': 0,
                'answer_id': 'term-time-location-answer'
            },
            {
                'group_instance': 0,
                'value': '',
                'answer_instance': 0,
                'answer_id': 'country-of-birth-wales-answer-other'
            },
            {
                'group_instance': 0,
                'value': 'England',
                'answer_instance': 0,
                'answer_id': 'country-of-birth-england-answer'
            },
            {
                'group_instance': 0,
                'value': '',
                'answer_instance': 0,
                'answer_id': 'country-of-birth-england-answer-other'
            },
            {
                'group_instance': 0,
                'value': 'Yes, 1 -19 hours a week',
                'answer_instance': 0,
                'answer_id': 'carer-answer'
            },
            {
                'group_instance': 0,
                'value': 'Ind',
                'answer_instance': 0,
                'answer_id': 'national-identity-england-answer-other'
            },
            {
                'group_instance': 0,
                'value': '',
                'answer_instance': 0,
                'answer_id': 'national-identity-wales-answer-other'
            },
            {
                'group_instance': 0,
                'value': [
                    'English',
                    'Welsh',
                    'Scottish',
                    'Northern Irish',
                    'British',
                    'Other'
                ],
                'answer_instance': 0,
                'answer_id': 'national-identity-england-answer'
            },
            {
                'group_instance': 0,
                'value': [],
                'answer_instance': 0,
                'answer_id': 'national-identity-wales-answer'
            },
            {
                'group_instance': 0,
                'value': 'Other ethnic group',
                'answer_instance': 0,
                'answer_id': 'ethnic-group-england-answer'
            },
            {
                'group_instance': 0,
                'value': 'Other',
                'answer_instance': 0,
                'answer_id': 'other-ethnic-group-answer'
            },
            {
                'group_instance': 0,
                'value': 'Telugu',
                'answer_instance': 0,
                'answer_id': 'other-ethnic-group-answer-other'
            },
            {
                'group_instance': 0,
                'value': '',
                'answer_instance': 0,
                'answer_id': 'language-welsh-answer-other'
            },
            {
                'group_instance': 0,
                'value': 'English',
                'answer_instance': 0,
                'answer_id': 'language-england-answer'
            },
            {
                'group_instance': 0,
                'value': '',
                'answer_instance': 0,
                'answer_id': 'language-england-answer-other'
            },
            {
                'group_instance': 0,
                'value': [],
                'answer_instance': 0,
                'answer_id': 'religion-welsh-answer'
            },
            {
                'group_instance': 0,
                'value': [
                    'No religion',
                    'Christian (Including Church of England, Catholic, Protestant and all other Christian denominations)',
                    'Buddhist',
                    'Hindu',
                    'Jewish',
                    'Muslim',
                    'Sikh',
                    'Other'
                ],
                'answer_instance': 0,
                'answer_id': 'religion-answer'
            },
            {
                'group_instance': 0,
                'value': '',
                'answer_instance': 0,
                'answer_id': 'religion-welsh-answer-other'
            },
            {
                'group_instance': 0,
                'value': 'Ind',
                'answer_instance': 0,
                'answer_id': 'religion-answer-other'
            },
            {
                'group_instance': 0,
                'value': 'This address',
                'answer_instance': 0,
                'answer_id': 'past-usual-address-answer'
            },
            {
                'group_instance': 0,
                'value': '',
                'answer_instance': 0,
                'answer_id': 'past-usual-address-answer-other'
            },
            {
                'group_instance': 0,
                'value': [
                    'United Kingdom'
                ],
                'answer_instance': 0,
                'answer_id': 'passports-answer'
            },
            {
                'group_instance': 0,
                'value': 'Yes, limited a lot',
                'answer_instance': 0,
                'answer_id': 'disability-answer'
            },
            {
                'group_instance': 0,
                'value': [
                    'Masters Degree',
                    'Postgraduate Certificate / Diploma'
                ],
                'answer_instance': 0,
                'answer_id': 'qualifications-england-answer'
            },
            {
                'group_instance': 0,
                'value': [],
                'answer_instance': 0,
                'answer_id': 'qualifications-welsh-answer'
            },
            {
                'group_instance': 0,
                'value': 'No',
                'answer_instance': 0,
                'answer_id': 'volunteering-answer'
            },
            {
                'group_instance': 0,
                'value': [
                    'none of the above?'
                ],
                'answer_instance': 0,
                'answer_id': 'employment-type-answer'
            },
            {
                'group_instance': 0,
                'value': 'Yes',
                'answer_instance': 0,
                'answer_id': 'jobseeker-answer'
            },
            {
                'group_instance': 0,
                'value': 'Yes',
                'answer_instance': 0,
                'answer_id': 'job-availability-answer'
            },
            {
                'group_instance': 0,
                'value': 'Yes',
                'answer_instance': 0,
                'answer_id': 'job-pending-answer'
            },
            {
                'group_instance': 0,
                'value': [
                    'a student?',
                    'long-term sick or disabled?'
                ],
                'answer_instance': 0,
                'answer_id': 'occupation-answer'
            },
            {
                'group_instance': 0,
                'value': 'Yes',
                'answer_instance': 0,
                'answer_id': 'ever-worked-answer'
            },
            {
                'group_instance': 0,
                'value': 'an employee?',
                'answer_instance': 0,
                'answer_id': 'main-job-answer'
            },
            {
                'group_instance': 0,
                'value': 'Software Engineer',
                'answer_instance': 0,
                'answer_id': 'job-title-answer'
            },
            {
                'group_instance': 0,
                'value': 'Development',
                'answer_instance': 0,
                'answer_id': 'job-description-answer'
            },
            {
                'group_instance': 0,
                'value': '31 - 48',
                'answer_instance': 0,
                'answer_id': 'hours-worked-answer'
            },
            {
                'group_instance': 0,
                'value': 'Train',
                'answer_instance': 0,
                'answer_id': 'work-travel-answer'
            },
            {
                'group_instance': 0,
                'value': 'Civil Servant',
                'answer_instance': 0,
                'answer_id': 'employers-business-answer'
            },
            {
                'group_instance': 0,
                'value': 'Employed by an organisation or business',
                'answer_instance': 0,
                'answer_id': 'main-job-type-answer'
            },
            {
                'group_instance': 0,
                'value': 'ONS',
                'answer_instance': 0,
                'answer_id': 'business-name-answer'
            }
        ]

        return expected_downstream_data

    def complete_survey(self, eq_id, form_type_id):
        variant_flags = {'sexual_identity': 'false'}
        self.launchSurvey(eq_id, form_type_id, region_code='GB-ENG', variant_flags=variant_flags, roles=['dumper'])

        # We are in the questionnaire
        self.assertInPage('What is your name?')
        self.assertInPage('>Save and continue<')

        post_data = [
            {
                'first-name': 'Danny',
                'middle-names': 'K',
                'last-name': 'Boje'
            },
            {
                'sex-answer': ['Male']
            },
            {
                'date-of-birth-answer-day': '12',
                'date-of-birth-answer-month': '5',
                'date-of-birth-answer-year': '1988',
            },
            {
                'marital-status-answer': ['In a registered same-sex civil partnership']
            },
            {
                'another-address-answer': ['Yes, an address within the UK']
            },
            {
                'other-address-answer-building': '12',
                'other-address-answer-city': 'Newport',
                'other-address-answer-postcode': 'NP10 8XG'
            },
            {
                'address-type-answer': ['Other'],
                'address-type-answer-other': 'Friends Home'
            },
            {
                'in-education-answer': ['Yes']
            },
            {
                'term-time-location-answer': ['here, at this address']
            },
            {
                'country-of-birth-england-answer': ['England']
            },
            {
                'carer-answer': ['Yes, 1 -19 hours a week']
            },
            {
                'national-identity-england-answer': ['English',
                                                     'Welsh',
                                                     'Scottish',
                                                     'Northern Irish',
                                                     'British',
                                                     'Other'],
                'national-identity-england-answer-other': 'Ind'
            },
            {
                'ethnic-group-england-answer': ['Other ethnic group']
            },
            {
                'other-ethnic-group-answer': ['Other'],
                'other-ethnic-group-answer-other': 'Telugu'
            },
            {
                'language-england-answer': ['English']
            },
            {
                'religion-answer': ['No religion',
                                    'Christian (Including Church of England, Catholic, Protestant and all other Christian denominations)',
                                    'Buddhist',
                                    'Hindu',
                                    'Jewish',
                                    'Muslim',
                                    'Sikh',
                                    'Other'],
                'religion-answer-other': 'Ind'
            },
            {
                'past-usual-address-answer': ['This address']
            },
            {
                'passports-answer': ['United Kingdom']
            },
            {
                'disability-answer': ['Yes, limited a lot']
            },
            {
                'qualifications-england-answer': ['Masters Degree',
                                                  'Postgraduate Certificate / Diploma']
            },
            {
                'volunteering-answer': ['No']
            },
            {
                'employment-type-answer': ['none of the above?']
            },
            {
                'jobseeker-answer': ['Yes']
            },
            {
                'job-availability-answer': ['Yes']
            },
            {
                'job-pending-answer': ['Yes']
            },
            {
                'occupation-answer': ['a student?',
                                      'long-term sick or disabled?']
            },
            {
                'ever-worked-answer': ['Yes']
            },
            {
                'main-job-answer': ['an employee?']
            },
            {
                'job-title-answer': 'Software Engineer'
            },
            {
                'job-description-answer': 'Development'
            },
            {
                'hours-worked-answer': ['31 - 48']
            },
            {
                'work-travel-answer': ['Train']
            },
            {
                'employers-business-answer': 'Civil Servant'
            },
            {
                'main-job-type-answer': ['Employed by an organisation or business']
            },
            {
                'business-name-answer': 'ONS'
            }
        ]
        for post in post_data:
            self.post(post_data=post)

        # There are no validation errors (we're on the summary screen)
        self.assertInPage('You’re ready to submit your 2017 Census Test')
