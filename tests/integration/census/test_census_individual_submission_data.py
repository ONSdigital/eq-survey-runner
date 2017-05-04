from tests.integration.integration_test_case import IntegrationTestCase


class TestCensusIndividualSubmissionData(IntegrationTestCase):

    def test_census_individual_data_matches_census_individual(self):
        self.complete_survey('census', 'individual')

        # Only verifying 'data'
        actual_downstream_data = self.dumpSubmission()['submission']['data']
        expected_downstream_data = self.get_expected_submission_data()

        self.assertCountEqual(actual_downstream_data, expected_downstream_data)

    @staticmethod
    def get_expected_submission_data():
        expected_downstream_data = [
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "Danny",
                "block_id": "correct-name",
                "answer_instance": 0,
                "answer_id": "first-name"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "K",
                "block_id": "correct-name",
                "answer_instance": 0,
                "answer_id": "middle-names"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "Boje",
                "block_id": "correct-name",
                "answer_instance": 0,
                "answer_id": "last-name"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "Male",
                "block_id": "sex",
                "answer_instance": 0,
                "answer_id": "sex-answer"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "12/05/1988",
                "block_id": "date-of-birth",
                "answer_instance": 0,
                "answer_id": "date-of-birth-answer"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "In a registered same-sex civil partnership",
                "block_id": "marital-status",
                "answer_instance": 0,
                "answer_id": "marital-status-answer"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "Yes, an address within the UK",
                "block_id": "another-address",
                "answer_instance": 0,
                "answer_id": "another-address-answer"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "",
                "block_id": "another-address",
                "answer_instance": 0,
                "answer_id": "another-address-answer-other"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "Newport",
                "block_id": "other-address",
                "answer_instance": 0,
                "answer_id": "other-address-answer-city"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "",
                "block_id": "other-address",
                "answer_instance": 0,
                "answer_id": "other-address-answer-street"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "",
                "block_id": "other-address",
                "answer_instance": 0,
                "answer_id": "other-address-answer-county"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "12",
                "block_id": "other-address",
                "answer_instance": 0,
                "answer_id": "other-address-answer-building"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "NP10 8XG",
                "block_id": "other-address",
                "answer_instance": 0,
                "answer_id": "other-address-answer-postcode"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "Friends Home",
                "block_id": "address-type",
                "answer_instance": 0,
                "answer_id": "address-type-answer-other"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "Other",
                "block_id": "address-type",
                "answer_instance": 0,
                "answer_id": "address-type-answer"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "Yes",
                "block_id": "in-education",
                "answer_instance": 0,
                "answer_id": "in-education-answer"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "here, at this address",
                "block_id": "term-time-location",
                "answer_instance": 0,
                "answer_id": "term-time-location-answer"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "",
                "block_id": "country-of-birth",
                "answer_instance": 0,
                "answer_id": "country-of-birth-wales-answer-other"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "England",
                "block_id": "country-of-birth",
                "answer_instance": 0,
                "answer_id": "country-of-birth-england-answer"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "",
                "block_id": "country-of-birth",
                "answer_instance": 0,
                "answer_id": "country-of-birth-england-answer-other"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "Yes, 1 -19 hours a week",
                "block_id": "carer",
                "answer_instance": 0,
                "answer_id": "carer-answer"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "Ind",
                "block_id": "national-identity",
                "answer_instance": 0,
                "answer_id": "national-identity-england-answer-other"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "",
                "block_id": "national-identity",
                "answer_instance": 0,
                "answer_id": "national-identity-wales-answer-other"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": [
                    "English",
                    "Welsh",
                    "Scottish",
                    "Northern Irish",
                    "British",
                    "Other"
                ],
                "block_id": "national-identity",
                "answer_instance": 0,
                "answer_id": "national-identity-england-answer"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": [],
                "block_id": "national-identity",
                "answer_instance": 0,
                "answer_id": "national-identity-wales-answer"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "Other ethnic group",
                "block_id": "ethnic-group",
                "answer_instance": 0,
                "answer_id": "ethnic-group-england-answer"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "Other",
                "block_id": "other-ethnic-group",
                "answer_instance": 0,
                "answer_id": "other-ethnic-group-answer"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "Telugu",
                "block_id": "other-ethnic-group",
                "answer_instance": 0,
                "answer_id": "other-ethnic-group-answer-other"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "",
                "block_id": "language",
                "answer_instance": 0,
                "answer_id": "language-welsh-answer-other"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "English",
                "block_id": "language",
                "answer_instance": 0,
                "answer_id": "language-england-answer"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "",
                "block_id": "language",
                "answer_instance": 0,
                "answer_id": "language-england-answer-other"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": [],
                "block_id": "religion",
                "answer_instance": 0,
                "answer_id": "religion-welsh-answer"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": [
                    "No religion",
                    "Christian (Including Church of England, Catholic, Protestant and all other Christian denominations)",
                    "Buddhist",
                    "Hindu",
                    "Jewish",
                    "Muslim",
                    "Sikh",
                    "Other"
                ],
                "block_id": "religion",
                "answer_instance": 0,
                "answer_id": "religion-answer"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "",
                "block_id": "religion",
                "answer_instance": 0,
                "answer_id": "religion-welsh-answer-other"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "Ind",
                "block_id": "religion",
                "answer_instance": 0,
                "answer_id": "religion-answer-other"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "This address",
                "block_id": "past-usual-address",
                "answer_instance": 0,
                "answer_id": "past-usual-address-answer"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "",
                "block_id": "past-usual-address",
                "answer_instance": 0,
                "answer_id": "past-usual-address-answer-other"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": [
                    "United Kingdom"
                ],
                "block_id": "passports",
                "answer_instance": 0,
                "answer_id": "passports-answer"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "Yes, limited a lot",
                "block_id": "disability",
                "answer_instance": 0,
                "answer_id": "disability-answer"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": [
                    "Masters Degree",
                    "Postgraduate Certificate / Diploma"
                ],
                "block_id": "qualifications",
                "answer_instance": 0,
                "answer_id": "qualifications-england-answer"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": [],
                "block_id": "qualifications",
                "answer_instance": 0,
                "answer_id": "qualifications-welsh-answer"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "No",
                "block_id": "volunteering",
                "answer_instance": 0,
                "answer_id": "volunteering-answer"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": [
                    "none of the above?"
                ],
                "block_id": "employment-type",
                "answer_instance": 0,
                "answer_id": "employment-type-answer"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "Yes",
                "block_id": "jobseeker",
                "answer_instance": 0,
                "answer_id": "jobseeker-answer"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "Yes",
                "block_id": "job-availability",
                "answer_instance": 0,
                "answer_id": "job-availability-answer"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "Yes",
                "block_id": "job-pending",
                "answer_instance": 0,
                "answer_id": "job-pending-answer"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": [
                    "a student?",
                    "long-term sick or disabled?"
                ],
                "block_id": "occupation",
                "answer_instance": 0,
                "answer_id": "occupation-answer"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "Yes",
                "block_id": "ever-worked",
                "answer_instance": 0,
                "answer_id": "ever-worked-answer"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "an employee?",
                "block_id": "main-job",
                "answer_instance": 0,
                "answer_id": "main-job-answer"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "Software Engineer",
                "block_id": "job-title",
                "answer_instance": 0,
                "answer_id": "job-title-answer"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "Development",
                "block_id": "job-description",
                "answer_instance": 0,
                "answer_id": "job-description-answer"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "Civil Servant",
                "block_id": "employers-business",
                "answer_instance": 0,
                "answer_id": "employers-business-answer"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "Employed by an organisation or business",
                "block_id": "main-job-type",
                "answer_instance": 0,
                "answer_id": "main-job-type-answer"
            },
            {
                "group_instance": 0,
                "group_id": "household-member",
                "value": "ONS",
                "block_id": "business-name",
                "answer_instance": 0,
                "answer_id": "business-name-answer"
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
