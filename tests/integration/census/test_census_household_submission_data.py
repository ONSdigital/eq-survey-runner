from mock import patch

from tests.integration.integration_test_case import IntegrationTestCase


# pylint: disable=too-many-lines
class TestCensusHouseholdSubmissionData(IntegrationTestCase):
    def test_census_household_data_matches_census_individual(self):
        with patch('app.helpers.schema_helpers.uuid4', side_effect=range(100)):
            self.complete_survey('census', 'household')

        # Only verifying 'data'
        actual_downstream_data = self.dumpSubmission()['submission']['data']

        expected_downstream_data = self.get_expected_submission_data()
        self.assertCountEqual(actual_downstream_data, expected_downstream_data)

    @staticmethod
    def get_expected_submission_data():
        expected_downstream_data = [
            {'value': 'west glamorgan',
             'answer_id': 'county',
             'answer_instance': 0,
             'group_instance_id': None,
             'group_instance': 0},
            {'value': 'wales',
             'answer_id': 'country',
             'answer_instance': 0,
             'group_instance_id': None,
             'group_instance': 0},
            {'value': '44 hill side',
             'answer_id': 'address-line-1',
             'answer_instance': 0,
             'group_instance_id': None,
             'group_instance': 0},
            {'value': '',
             'answer_id': 'address-line-3',
             'answer_instance': 0,
             'group_instance_id': None,
             'group_instance': 0},
            {'value': 'cimla',
             'answer_id': 'address-line-2',
             'answer_instance': 0,
             'group_instance_id': None,
             'group_instance': 0},
            {'value': 'neath',
             'answer_id': 'town-city',
             'answer_instance': 0,
             'group_instance_id': None,
             'group_instance': 0},
            {'value': 'cf336gn',
             'answer_id': 'postcode',
             'answer_instance': 0,
             'group_instance_id': None,
             'group_instance': 0},
            {'value': 'Yes',
             'answer_id': 'permanent-or-family-home-answer',
             'answer_instance': 0,
             'group_instance_id': None,
             'group_instance': 0},
            {'value': 'K',
             'answer_id': 'middle-names',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': 'Boje',
             'answer_id': 'last-name',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': 'Danny',
             'answer_id': 'first-name',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': 'K',
             'answer_id': 'middle-names',
             'answer_instance': 1,
             'group_instance_id': '3',
             'group_instance': 0},
            {'value': 'Yo',
             'answer_id': 'last-name',
             'answer_instance': 1,
             'group_instance_id': '3',
             'group_instance': 0},
            {'value': 'Anjali',
             'answer_id': 'first-name',
             'answer_instance': 1,
             'group_instance_id': '3',
             'group_instance': 0},
            {'value': 'Yes',
             'answer_id': 'everyone-at-address-confirmation-answer',
             'answer_instance': 0,
             'group_instance_id': None,
             'group_instance': 0},
            {'value': 2,
             'answer_id': 'overnight-visitors-answer',
             'answer_instance': 0,
             'group_instance_id': None,
             'group_instance': 0},
            {'value': 'Husband or wife',
             'answer_id': 'household-relationships-answer',
             'answer_instance': 0,
             'group_instance_id': None,
             'group_instance': 0},
            {'value': 'Whole house or bungalow',
             'answer_id': 'type-of-accommodation-answer',
             'answer_instance': 0,
             'group_instance_id': None,
             'group_instance': 0},
            {'value': 'Detached',
             'answer_id': 'type-of-house-answer',
             'answer_instance': 0,
             'group_instance_id': None,
             'group_instance': 0},
            {'value': 'No',
             'answer_id': 'self-contained-accommodation-answer',
             'answer_instance': 0,
             'group_instance_id': None,
             'group_instance': 0},
            {'value': 2,
             'answer_id': 'number-of-bedrooms-answer',
             'answer_instance': 0,
             'group_instance_id': None,
             'group_instance': 0},
            {'value': ['Gas',
                       'Electric (include storage heaters)',
                       'Oil',
                       'Solid fuel (for example wood, coal)',
                       'Renewable (for example solar panels)',
                       'Other central heating',
                       'No central heating'],
             'answer_id': 'central-heating-answer',
             'answer_instance': 0,
             'group_instance_id': None,
             'group_instance': 0},
            {'value': 'Owns outright',
             'answer_id': 'own-or-rent-answer',
             'answer_instance': 0,
             'group_instance_id': None,
             'group_instance': 0},
            {'value': 2,
             'answer_id': 'number-of-vehicles-answer',
             'answer_instance': 0,
             'group_instance_id': None,
             'group_instance': 0},
            {'value': 'Yes',
             'answer_id': 'over-16-answer',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': 'No, I do not want to request a personal form',
             'answer_id': 'private-response-answer',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': 'Male',
             'answer_id': 'sex-answer',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': '1988-05-12',
             'answer_id': 'date-of-birth-answer',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': 'In a registered same-sex civil partnership',
             'answer_id': 'marital-status-answer',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': '',
             'answer_id': 'another-address-answer-other',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': 'Yes, an address within the UK',
             'answer_id': 'another-address-answer',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': '',
             'answer_id': 'other-address-answer-street',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': 'NP10 8XG',
             'answer_id': 'other-address-answer-postcode',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': '',
             'answer_id': 'other-address-answer-county',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': 'Newport',
             'answer_id': 'other-address-answer-city',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': '12',
             'answer_id': 'other-address-answer-building',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': 'Other',
             'answer_id': 'address-type-answer',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': 'Friends Home',
             'answer_id': 'address-type-answer-other',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': 'Yes',
             'answer_id': 'in-education-answer',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': 'Yes',
             'answer_id': 'term-time-location-answer',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': '',
             'answer_id': 'country-of-birth-wales-answer-other',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': 'England',
             'answer_id': 'country-of-birth-england-answer',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': '',
             'answer_id': 'country-of-birth-england-answer-other',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': 'Yes, 1 -19 hours a week',
             'answer_id': 'carer-answer',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': [],
             'answer_id': 'national-identity-wales-answer',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': '',
             'answer_id': 'national-identity-wales-answer-other',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': 'Ind',
             'answer_id': 'national-identity-england-answer-other',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': ['English',
                       'Welsh',
                       'Scottish',
                       'Northern Irish',
                       'British',
                       'Other'],
             'answer_id': 'national-identity-england-answer',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': 'Other ethnic group',
             'answer_id': 'ethnic-group-england-answer',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': 'Other',
             'answer_id': 'other-ethnic-group-answer',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': 'Telugu',
             'answer_id': 'other-ethnic-group-answer-other',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': '',
             'answer_id': 'language-england-answer-other',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': 'English',
             'answer_id': 'language-england-answer',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': '',
             'answer_id': 'language-welsh-answer-other',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': 'Ind',
             'answer_id': 'religion-answer-other',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': ['No religion',
                       'Buddhism',
                       'Hinduism',
                       'Judaism',
                       'Islam',
                       'Sikhism',
                       'Other'],
             'answer_id': 'religion-answer',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': 'This address',
             'answer_id': 'past-usual-address-answer',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': '',
             'answer_id': 'past-usual-address-answer-other',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': ['United Kingdom'],
             'answer_id': 'passports-answer',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': 'Yes, limited a lot',
             'answer_id': 'disability-answer',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': ['Masters Degree',
                       'Postgraduate Certificate / Diploma'],
             'answer_id': 'qualifications-england-answer',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': [],
             'answer_id': 'qualifications-welsh-answer',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': ['none of the above'],
             'answer_id': 'employment-type-answer',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': 'Yes',
             'answer_id': 'jobseeker-answer',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': 'Yes',
             'answer_id': 'job-availability-answer',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': 'Yes',
             'answer_id': 'job-pending-answer',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': ['a student',
                       'long-term sick or disabled'],
             'answer_id': 'occupation-answer',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': 'Yes',
             'answer_id': 'ever-worked-answer',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': 'an employee',
             'answer_id': 'main-job-answer',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': '31 - 48',
             'answer_id': 'hours-worked-answer',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': 'Train',
             'answer_id': 'work-travel-answer',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': 'Software Engineer',
             'answer_id': 'job-title-answer',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': 'Development',
             'answer_id': 'job-description-answer',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': 'Employed by an organisation or business',
             'answer_id': 'main-job-type-answer',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': 'ONS',
             'answer_id': 'business-name-answer',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': 'Civil Servant',
             'answer_id': 'employers-business-answer',
             'answer_instance': 0,
             'group_instance_id': '2',
             'group_instance': 0},
            {'value': 'Yes',
             'answer_id': 'over-16-answer',
             'answer_instance': 0,
             'group_instance_id': '3',
             'group_instance': 1},
            {'value': 'Yes, I want to request a personal form',
             'answer_id': 'private-response-answer',
             'answer_instance': 0,
             'group_instance_id': '3',
             'group_instance': 1},
            {'value': 'K',
             'answer_id': 'visitor-last-name',
             'answer_instance': 0,
             'group_instance_id': None,
             'group_instance': 0},
            {'value': 'Diya',
             'answer_id': 'visitor-first-name',
             'answer_instance': 0,
             'group_instance_id': None,
             'group_instance': 0},
            {'value': 'Female',
             'answer_id': 'visitor-sex-answer',
             'answer_instance': 0,
             'group_instance_id': None,
             'group_instance': 0},
            {'value': '2016-11-04',
             'answer_id': 'visitor-date-of-birth-answer',
             'answer_instance': 0,
             'group_instance_id': None,
             'group_instance': 0},
            {'value': 'Yes, usually lives in the United Kingdom',
             'answer_id': 'visitor-uk-resident-answer',
             'answer_instance': 0,
             'group_instance_id': None,
             'group_instance': 0},
            {'value': '',
             'answer_id': 'visitor-uk-resident-answer-other',
             'answer_instance': 0,
             'group_instance_id': None,
             'group_instance': 0},
            {'value': 'Vizag',
             'answer_id': 'visitor-address-answer-city',
             'answer_instance': 0,
             'group_instance_id': None,
             'group_instance': 0},
            {'value': '',
             'answer_id': 'visitor-address-answer-county',
             'answer_instance': 0,
             'group_instance_id': None,
             'group_instance': 0},
            {'value': '',
             'answer_id': 'visitor-address-answer-street',
             'answer_instance': 0,
             'group_instance_id': None,
             'group_instance': 0},
            {'value': '530003',
             'answer_id': 'visitor-address-answer-postcode',
             'answer_instance': 0,
             'group_instance_id': None,
             'group_instance': 0},
            {'value': '309',
             'answer_id': 'visitor-address-answer-building',
             'answer_instance': 0,
             'group_instance_id': None,
             'group_instance': 0},
            {'value': 'K',
             'answer_id': 'visitor-last-name',
             'answer_instance': 0,
             'group_instance_id': None,
             'group_instance': 1},
            {'value': 'Niki',
             'answer_id': 'visitor-first-name',
             'answer_instance': 0,
             'group_instance_id': None,
             'group_instance': 1},
            {'value': 'Male',
             'answer_id': 'visitor-sex-answer',
             'answer_instance': 0,
             'group_instance_id': None,
             'group_instance': 1},
            {'value': '1985-10-17',
             'answer_id': 'visitor-date-of-birth-answer',
             'answer_instance': 0,
             'group_instance_id': None,
             'group_instance': 1},
            {'value': 'Yes, usually lives in the United Kingdom',
             'answer_id': 'visitor-uk-resident-answer',
             'answer_instance': 0,
             'group_instance_id': None,
             'group_instance': 1},
            {'value': '',
             'answer_id': 'visitor-uk-resident-answer-other',
             'answer_instance': 0,
             'group_instance_id': None,
             'group_instance': 1},
            {'value': 'Detroit',
             'answer_id': 'visitor-address-answer-city',
             'answer_instance': 0,
             'group_instance_id': None,
             'group_instance': 1},
            {'value': '',
             'answer_id': 'visitor-address-answer-county',
             'answer_instance': 0,
             'group_instance_id': None,
             'group_instance': 1},
            {'value': '',
             'answer_id': 'visitor-address-answer-street',
             'answer_instance': 0,
             'group_instance_id': None,
             'group_instance': 1},
            {'value': '12345',
             'answer_id': 'visitor-address-answer-postcode',
             'answer_instance': 0,
             'group_instance_id': None,
             'group_instance': 1},
            {'value': '1009',
             'answer_id': 'visitor-address-answer-building',
             'answer_instance': 0,
             'group_instance_id': None,
             'group_instance': 1}
        ]

        return expected_downstream_data

    def complete_survey(self, eq_id, form_type_id):
        self.launchSurvey(eq_id, form_type_id, region_code='GB-ENG', sexual_identity=False, roles=['dumper'])

        self.post(action='start_questionnaire')

        self.complete_who_lives_here_section()

        self.complete_household_and_accommodation_section()

        self.complete_individual_section_person_1()

        self.complete_individual_section_person_2()

        self.complete_visitors_section_visitor_1()

        self.complete_visitors_section_visitor_2()

        # There are no validation errors (we're on the summary screen)
        self.assertInPage('You’re ready to submit your 2017 Census Test')

    def complete_visitors_section_visitor_1(self):
        # Start of Visitors section
        post_data = [
            {
                'visitor-first-name': 'Diya',
                'visitor-last-name': 'K'
            },
            {
                'visitor-sex-answer': ['Female']
            },
            {
                'visitor-date-of-birth-answer-day': '4',
                'visitor-date-of-birth-answer-month': '11',
                'visitor-date-of-birth-answer-year': '2016',
            },
            {
                'visitor-uk-resident-answer': ['Yes, usually lives in the United Kingdom']
            },
            {
                'visitor-address-answer-building': '309',
                'visitor-address-answer-city': 'Vizag',
                'visitor-address-answer-postcode': '530003'
            },
        ]

        for post in post_data:
            self.post(post_data=post)

        self.assertInPage('You have completed all questions for Visitor 1')
        self.post(action='save_continue')

    def complete_visitors_section_visitor_2(self):
        post_data = [
            {
                'visitor-first-name': 'Niki',
                'visitor-last-name': 'K'
            },
            {
                'visitor-sex-answer': ['Male']
            },
            {
                'visitor-date-of-birth-answer-day': '17',
                'visitor-date-of-birth-answer-month': '10',
                'visitor-date-of-birth-answer-year': '1985',
            },
            {
                'visitor-uk-resident-answer': ['Yes, usually lives in the United Kingdom']
            },
            {
                'visitor-address-answer-building': '1009',
                'visitor-address-answer-city': 'Detroit',
                'visitor-address-answer-postcode': '12345'
            },
        ]
        for post in post_data:
            self.post(post_data=post)

        # Completed Visitors sections
        self.assertInPage('You have completed all questions for Visitor 2')
        self.post(action='save_continue')
        self.assertInPage('You have successfully completed the ‘Visitors’ section')
        self.post(action='save_continue')

    def complete_individual_section_person_1(self):
        # Start of Individual section questions for Person 1
        self.post(action='save_continue')
        post_data = [
            {
                'details-correct-answer': ['Yes, this is my full name']
            },
            {
                'over-16-answer': ['Yes']
            },
            {
                'private-response-answer': ['No, I do not want to request a personal form']
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
                'term-time-location-answer': ['Yes']
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
                                    'Buddhism',
                                    'Hinduism',
                                    'Judaism',
                                    'Islam',
                                    'Sikhism',
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
                'employment-type-answer': ['none of the above']
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
                'occupation-answer': ['a student',
                                      'long-term sick or disabled']
            },
            {
                'ever-worked-answer': ['Yes']
            },
            {
                'main-job-answer': ['an employee']
            },
            {
                'hours-worked-answer': ['31 - 48']
            },
            {
                'work-travel-answer': ['Train']
            },
            {
                'job-title-answer': 'Software Engineer'
            },
            {
                'job-description-answer': 'Development'
            },
            {
                'main-job-type-answer': ['Employed by an organisation or business']
            },
            {
                'business-name-answer': 'ONS'
            },
            {
                'employers-business-answer': 'Civil Servant'
            }
        ]
        for post in post_data:
            self.post(post_data=post)

        # Completed Individual section questions for person 1
        self.assertInPage('There are no more questions for Danny Boje')
        self.post(action='save_continue')
        self.assertInPage('Anjali Yo')
        self.post(action='save_continue')

    def complete_individual_section_person_2(self):
        # Start of Individual section questions for Person 2
        self.post(action='save_continue')
        post_data = [
            {
                'details-correct-answer': ['Yes, this is my full name']
            },
            {
                'over-16-answer': ['Yes']
            },
            {
                'private-response-answer': ['Yes, I want to request a personal form']
            }
        ]
        for post in post_data:
            self.post(post_data=post)

        self.assertInPage('Request for personal and confidential form')
        self.post(action='save_continue')

        # Completed Individual section
        self.assertInPage('There are no more questions for Anjali Yo')
        self.post(action='save_continue')
        self.assertInPage('Name of visitor')
        self.post(action='save_continue')

    def complete_household_and_accommodation_section(self):
        # Start of Household and Accommodation section
        self.post(action='save_continue')
        post_data = [
            {
                'type-of-accommodation-answer': ['Whole house or bungalow']
            },
            {
                'type-of-house-answer': ['Detached']
            },
            {
                'self-contained-accommodation-answer': ['No']
            },
            {
                'number-of-bedrooms-answer': '2'
            },
            {
                'central-heating-answer': [
                    'Gas',
                    'Electric (include storage heaters)',
                    'Oil',
                    'Solid fuel (for example wood, coal)',
                    'Renewable (for example solar panels)',
                    'Other central heating',
                    'No central heating'
                ]
            },
            {
                'own-or-rent-answer': ['Owns outright']
            },
            {
                'number-of-vehicles-answer': '2'
            },
        ]
        for post in post_data:
            self.post(post_data=post)

        # Completed Household and Accommodation section
        self.assertInPage('You have successfully completed the ‘Household and Accommodation’ section')
        self.post(action='save_continue')
        self.assertInPage('Danny Boje')
        self.post(action='save_continue')

    def complete_who_lives_here_section(self):
        # We are in the questionnaire
        self.assertInPage('What is your address?')
        self.assertInPage('Who lives here?')
        self.assertInPage('>Save and continue<')
        # In Who lives here? Section

        self.post(post_data={'permanent-or-family-home-answer': ['Yes']})
        self.post(action='add_answer')
        post_data = [
            {
                'address-line-1': '44 hill side',
                'address-line-2': 'cimla',
                'county': 'west glamorgan',
                'country': 'wales',
                'postcode': 'cf336gn',
                'town-city': 'neath'
            }
        ]

        for post in post_data:
            self.post(post_data=post)

        self.post(action='save_continue')

        post_data = [
            {
                'permanent-or-family-home-answer': ['Yes']
            },
            {
                # Person 1
                'household-0-first-name': 'Danny',
                'household-0-middle-names': 'K',
                'household-0-last-name': 'Boje',
                # Person 2
                'household-1-first-name': 'Anjali',
                'household-1-middle-names': 'K',
                'household-1-last-name': 'Yo'
            },
            {
                'everyone-at-address-confirmation-answer': ['Yes']
            },
            {
                'overnight-visitors-answer': '2'
            },
            {
                'household-relationships-answer-0': 'Husband or wife'
            }
        ]
        for post in post_data:
            self.post(post_data=post)

        # Completed Who lives here? Section
        self.assertInPage('You have successfully completed the ‘Who lives here?’ section')
        self.post(action='save_continue')
