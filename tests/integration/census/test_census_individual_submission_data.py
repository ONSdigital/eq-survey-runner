from mock import patch

from tests.integration.integration_test_case import IntegrationTestCase


class TestCensusIndividualSubmissionData(IntegrationTestCase):

    def test_census_individual_data_matches_census_individual(self):
        with patch('app.helpers.schema_helpers.uuid4', side_effect=range(100)):
            self.complete_survey('census', 'individual')

        # Only verifying 'data'
        actual_downstream_data = self.dumpSubmission()['submission']['data']
        expected_downstream_data = self.get_expected_submission_data()

        self.assertCountEqual(actual_downstream_data, expected_downstream_data)

    @staticmethod
    def get_expected_submission_data():
        expected_downstream_data = [
            {'answer_id': 'middle-names',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': 'K'},
            {'answer_id': 'last-name',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': 'Boje'},
            {'answer_id': 'first-name',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': 'Danny'},
            {'answer_id': 'sex-answer',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': 'Male'},
            {'answer_id': 'date-of-birth-answer',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': '1988-05-12'},
            {'answer_id': 'marital-status-answer',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': 'In a registered same-sex civil partnership'},
            {'answer_id': 'another-address-answer-other',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': ''},
            {'answer_id': 'another-address-answer',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': 'Yes, an address within the UK'},
            {'answer_id': 'other-address-answer-street',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': ''},
            {'answer_id': 'other-address-answer-postcode',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': 'NP10 8XG'},
            {'answer_id': 'other-address-answer-building',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': '12'},
            {'answer_id': 'other-address-answer-county',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': ''},
            {'answer_id': 'other-address-answer-city',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': 'Newport'},
            {'answer_id': 'address-type-answer',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': 'Other'},
            {'answer_id': 'address-type-answer-other',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': 'Friends Home'},
            {'answer_id': 'in-education-answer',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': 'Yes'},
            {'answer_id': 'term-time-location-answer',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': 'here, at this address'},
            {'answer_id': 'country-of-birth-england-answer-other',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': ''},
            {'answer_id': 'country-of-birth-wales-answer-other',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': ''},
            {'answer_id': 'country-of-birth-england-answer',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': 'England'},
            {'answer_id': 'carer-answer',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': 'Yes, 1 -19 hours a week'},
            {'answer_id': 'national-identity-england-answer-other',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': 'Ind'},
            {'answer_id': 'national-identity-wales-answer-other',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': ''},
            {'answer_id': 'national-identity-england-answer',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': ['English',
                       'Welsh',
                       'Scottish',
                       'Northern Irish',
                       'British',
                       'Other']},
            {'answer_id': 'national-identity-wales-answer',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': []},
            {'answer_id': 'ethnic-group-england-answer',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': 'Other ethnic group'},
            {'answer_id': 'other-ethnic-group-answer-other',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': 'Telugu'},
            {'answer_id': 'other-ethnic-group-answer',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': 'Other'},
            {'answer_id': 'language-welsh-answer-other',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': ''},
            {'answer_id': 'language-england-answer-other',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': ''},
            {'answer_id': 'language-england-answer',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': 'English'},
            {'answer_id': 'religion-answer',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': ['No religion',
                       'Christian (Including Church of England, Catholic, Protestant '
                       'and all other Christian denominations)',
                       'Buddhist',
                       'Hindu',
                       'Jewish',
                       'Muslim',
                       'Sikh',
                       'Other']},
            {'answer_id': 'religion-welsh-answer-other',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': ''},
            {'answer_id': 'religion-welsh-answer',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': []},
            {'answer_id': 'religion-answer-other',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': 'Ind'},
            {'answer_id': 'past-usual-address-answer',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': 'This address'},
            {'answer_id': 'past-usual-address-answer-other',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': ''},
            {'answer_id': 'passports-answer',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': ['United Kingdom']},
            {'answer_id': 'disability-answer',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': 'Yes, limited a lot'},
            {'answer_id': 'qualifications-welsh-answer',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': []},
            {'answer_id': 'qualifications-england-answer',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': ['Masters Degree', 'Postgraduate Certificate / Diploma']},
            {'answer_id': 'volunteering-answer',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': 'No'},
            {'answer_id': 'employment-type-answer',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': ['none of the above?']},
            {'answer_id': 'jobseeker-answer',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': 'Yes'},
            {'answer_id': 'job-availability-answer',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': 'Yes'},
            {'answer_id': 'job-pending-answer',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': 'Yes'},
            {'answer_id': 'occupation-answer',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': ['a student?', 'long-term sick or disabled?']},
            {'answer_id': 'ever-worked-answer',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': 'Yes'},
            {'answer_id': 'main-job-answer',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': 'an employee?'},
            {'answer_id': 'job-title-answer',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': 'Software Engineer'},
            {'answer_id': 'job-description-answer',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': 'Development'},
            {'answer_id': 'hours-worked-answer',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': '31 - 48'},
            {'answer_id': 'work-travel-answer',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': 'Train'},
            {'answer_id': 'employers-business-answer',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': 'Civil Servant'},
            {'answer_id': 'main-job-type-answer',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': 'Employed by an organisation or business'},
            {'answer_id': 'business-name-answer',
             'answer_instance': 0,
             'group_instance': 0,
             'group_instance_id': None,
             'value': 'ONS'}
        ]

        return expected_downstream_data

    def complete_survey(self, eq_id, form_type_id):
        self.launchSurvey(eq_id, form_type_id, region_code='GB-ENG', sexual_identity=False, roles=['dumper'])

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
