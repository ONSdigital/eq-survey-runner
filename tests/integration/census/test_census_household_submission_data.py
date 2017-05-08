from tests.integration.integration_test_case import IntegrationTestCase


class TestCensusHouseholdSubmissionData(IntegrationTestCase):

    def test_census_household_data_matches_census_individual(self):
        self.complete_survey('census', 'household')

        # Only verifying 'data'
        actual_downstream_data = self.dumpSubmission()['submission']['data']
        expected_downstream_data = self.get_expected_submission_data()

        self.assertCountEqual(actual_downstream_data, expected_downstream_data)

    @staticmethod
    def get_expected_submission_data():
        expected_downstream_data = [
            {
                "group_instance": 0,
                "answer_id": "permanent-or-family-home-answer",
                "block_id": "permanent-or-family-home",
                "group_id": "who-lives-here",
                "answer_instance": 0,
                "value": "Yes"
            },
            {
                "group_instance": 0,
                "answer_id": "middle-names",
                "block_id": "household-composition",
                "group_id": "who-lives-here",
                "answer_instance": 0,
                "value": "K"
            },
            {
                "group_instance": 0,
                "answer_id": "first-name",
                "block_id": "household-composition",
                "group_id": "who-lives-here",
                "answer_instance": 0,
                "value": "Danny"
            },
            {
                "group_instance": 0,
                "answer_id": "last-name",
                "block_id": "household-composition",
                "group_id": "who-lives-here",
                "answer_instance": 0,
                "value": "Boje"
            },
            {
                "group_instance": 0,
                "answer_id": "middle-names",
                "block_id": "household-composition",
                "group_id": "who-lives-here",
                "answer_instance": 1,
                "value": "K"
            },
            {
                "group_instance": 0,
                "answer_id": "first-name",
                "block_id": "household-composition",
                "group_id": "who-lives-here",
                "answer_instance": 1,
                "value": "Anjali"
            },
            {
                "group_instance": 0,
                "answer_id": "last-name",
                "block_id": "household-composition",
                "group_id": "who-lives-here",
                "answer_instance": 1,
                "value": "Yo"
            },
            {
                "group_instance": 0,
                "answer_id": "everyone-at-address-confirmation-answer",
                "block_id": "everyone-at-address-confirmation",
                "group_id": "who-lives-here",
                "answer_instance": 0,
                "value": "Yes"
            },
            {
                "group_instance": 0,
                "answer_id": "overnight-visitors-answer",
                "block_id": "overnight-visitors",
                "group_id": "who-lives-here",
                "answer_instance": 0,
                "value": 2
            },
            {
                "group_instance": 0,
                "answer_id": "household-relationships-answer",
                "block_id": "household-relationships",
                "group_id": "who-lives-here-relationship",
                "answer_instance": 0,
                "value": "Husband or wife"
            },
            {
                "group_instance": 0,
                "answer_id": "type-of-accommodation-answer",
                "block_id": "type-of-accommodation",
                "group_id": "household-and-accommodation",
                "answer_instance": 0,
                "value": "Whole house or bungalow"
            },
            {
                "group_instance": 0,
                "answer_id": "type-of-house-answer",
                "block_id": "type-of-house",
                "group_id": "household-and-accommodation",
                "answer_instance": 0,
                "value": "Detached"
            },
            {
                "group_instance": 0,
                "answer_id": "self-contained-accommodation-answer",
                "block_id": "self-contained-accommodation",
                "group_id": "household-and-accommodation",
                "answer_instance": 0,
                "value": "No"
            },
            {
                "group_instance": 0,
                "answer_id": "number-of-bedrooms-answer",
                "block_id": "number-of-bedrooms",
                "group_id": "household-and-accommodation",
                "answer_instance": 0,
                "value": 2
            },
            {
                "group_instance": 0,
                "answer_id": "central-heating-answer",
                "block_id": "central-heating",
                "group_id": "household-and-accommodation",
                "answer_instance": 0,
                "value": [
                    "No central heating",
                    "Gas",
                    "Electric (including storage heaters)",
                    "Oil",
                    "Solid fuel (for example wood, coal)",
                    "Other central heating"
                ]
            },
            {
                "group_instance": 0,
                "answer_id": "own-or-rent-answer",
                "block_id": "own-or-rent",
                "group_id": "household-and-accommodation",
                "answer_instance": 0,
                "value": "Owns outright"
            },
            {
                "group_instance": 0,
                "answer_id": "number-of-vehicles-answer",
                "block_id": "number-of-vehicles",
                "group_id": "household-and-accommodation",
                "answer_instance": 0,
                "value": 2
            },
            {
                "group_instance": 0,
                "answer_id": "details-correct-answer",
                "block_id": "details-correct",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": "Yes, this is my full name"
            },
            {
                "group_instance": 0,
                "answer_id": "over-16-answer",
                "block_id": "over-16",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": "Yes"
            },
            {
                "group_instance": 0,
                "answer_id": "private-response-answer",
                "block_id": "private-response",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": "No, I do not want to request a personal form"
            },
            {
                "group_instance": 0,
                "answer_id": "sex-answer",
                "block_id": "sex",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": "Male"
            },
            {
                "group_instance": 0,
                "answer_id": "date-of-birth-answer",
                "block_id": "date-of-birth",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": "12/05/1988"
            },
            {
                "group_instance": 0,
                "answer_id": "marital-status-answer",
                "block_id": "marital-status",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": "In a registered same-sex civil partnership"
            },
            {
                "group_instance": 0,
                "answer_id": "another-address-answer",
                "block_id": "another-address",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": "Yes, an address within the UK"
            },
            {
                "group_instance": 0,
                "answer_id": "another-address-answer-other",
                "block_id": "another-address",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": ""
            },
            {
                "group_instance": 0,
                "answer_id": "other-address-answer-building",
                "block_id": "other-address",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": "12"
            },
            {
                "group_instance": 0,
                "answer_id": "other-address-answer-street",
                "block_id": "other-address",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": ""
            },
            {
                "group_instance": 0,
                "answer_id": "other-address-answer-city",
                "block_id": "other-address",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": "Newport"
            },
            {
                "group_instance": 0,
                "answer_id": "other-address-answer-county",
                "block_id": "other-address",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": ""
            },
            {
                "group_instance": 0,
                "answer_id": "other-address-answer-postcode",
                "block_id": "other-address",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": "NP10 8XG"
            },
            {
                "group_instance": 0,
                "answer_id": "address-type-answer",
                "block_id": "address-type",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": "Other"
            },
            {
                "group_instance": 0,
                "answer_id": "address-type-answer-other",
                "block_id": "address-type",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": "Friends Home"
            },
            {
                "group_instance": 0,
                "answer_id": "in-education-answer",
                "block_id": "in-education",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": "Yes"
            },
            {
                "group_instance": 0,
                "answer_id": "term-time-location-answer",
                "block_id": "term-time-location",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": "here, at this address"
            },
            {
                "group_instance": 0,
                "answer_id": "country-of-birth-england-answer-other",
                "block_id": "country-of-birth",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": ""
            },
            {
                "group_instance": 0,
                "answer_id": "country-of-birth-england-answer",
                "block_id": "country-of-birth",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": "England"
            },
            {
                "group_instance": 0,
                "answer_id": "country-of-birth-wales-answer-other",
                "block_id": "country-of-birth",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": ""
            },
            {
                "group_instance": 0,
                "answer_id": "carer-answer",
                "block_id": "carer",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": "Yes, 1 -19 hours a week"
            },
            {
                "group_instance": 0,
                "answer_id": "national-identity-england-answer",
                "block_id": "national-identity",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": [
                    "English",
                    "Welsh",
                    "Scottish",
                    "Northern Irish",
                    "British",
                    "Other"
                ]
            },
            {
                "group_instance": 0,
                "answer_id": "national-identity-wales-answer",
                "block_id": "national-identity",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": []
            },
            {
                "group_instance": 0,
                "answer_id": "national-identity-wales-answer-other",
                "block_id": "national-identity",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": ""
            },
            {
                "group_instance": 0,
                "answer_id": "national-identity-england-answer-other",
                "block_id": "national-identity",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": "Ind"
            },
            {
                "group_instance": 0,
                "answer_id": "ethnic-group-england-answer",
                "block_id": "ethnic-group",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": "Other ethnic group"
            },
            {
                "group_instance": 0,
                "answer_id": "other-ethnic-group-answer",
                "block_id": "other-ethnic-group",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": "Other"
            },
            {
                "group_instance": 0,
                "answer_id": "other-ethnic-group-answer-other",
                "block_id": "other-ethnic-group",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": "Telugu"
            },
            {
                "group_instance": 0,
                "answer_id": "language-england-answer-other",
                "block_id": "language",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": ""
            },
            {
                "group_instance": 0,
                "answer_id": "language-england-answer",
                "block_id": "language",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": "English"
            },
            {
                "group_instance": 0,
                "answer_id": "language-welsh-answer-other",
                "block_id": "language",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": ""
            },
            {
                "group_instance": 0,
                "answer_id": "religion-welsh-answer-other",
                "block_id": "religion",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": ""
            },
            {
                "group_instance": 0,
                "answer_id": "religion-welsh-answer",
                "block_id": "religion",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": []
            },
            {
                "group_instance": 0,
                "answer_id": "religion-answer",
                "block_id": "religion",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": [
                    "No religion",
                    "Buddhist",
                    "Hindu",
                    "Jewish",
                    "Muslim",
                    "Sikh",
                    "Other"
                ]
            },
            {
                "group_instance": 0,
                "answer_id": "religion-answer-other",
                "block_id": "religion",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": "Ind"
            },
            {
                "group_instance": 0,
                "answer_id": "past-usual-address-answer",
                "block_id": "past-usual-address",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": "This address"
            },
            {
                "group_instance": 0,
                "answer_id": "past-usual-address-answer-other",
                "block_id": "past-usual-address",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": ""
            },
            {
                "group_instance": 0,
                "answer_id": "passports-answer",
                "block_id": "passports",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": [
                    "United Kingdom"
                ]
            },
            {
                "group_instance": 0,
                "answer_id": "disability-answer",
                "block_id": "disability",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": "Yes, limited a lot"
            },
            {
                "group_instance": 0,
                "answer_id": "qualifications-welsh-answer",
                "block_id": "qualifications",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": []
            },
            {
                "group_instance": 0,
                "answer_id": "qualifications-england-answer",
                "block_id": "qualifications",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": [
                    "Masters Degree",
                    "Postgraduate Certificate / Diploma"
                ]
            },
            {
                "group_instance": 0,
                "answer_id": "volunteering-answer",
                "block_id": "volunteering",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": "No"
            },
            {
                "group_instance": 0,
                "answer_id": "employment-type-answer",
                "block_id": "employment-type",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": [
                    "none of the above?"
                ]
            },
            {
                "group_instance": 0,
                "answer_id": "jobseeker-answer",
                "block_id": "jobseeker",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": "Yes"
            },
            {
                "group_instance": 0,
                "answer_id": "job-availability-answer",
                "block_id": "job-availability",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": "Yes"
            },
            {
                "group_instance": 0,
                "answer_id": "job-pending-answer",
                "block_id": "job-pending",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": "Yes"
            },
            {
                "group_instance": 0,
                "answer_id": "occupation-answer",
                "block_id": "occupation",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": [
                    "a student?",
                    "long-term sick or disabled?"
                ]
            },
            {
                "group_instance": 0,
                "answer_id": "ever-worked-answer",
                "block_id": "ever-worked",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": "Yes"
            },
            {
                "group_instance": 0,
                "answer_id": "main-job-answer",
                "block_id": "main-job",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": "an employee?"
            },
            {
                "group_instance": 0,
                "answer_id": "job-title-answer",
                "block_id": "job-title",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": "Software Engineer"
            },
            {
                "group_instance": 0,
                "answer_id": "job-description-answer",
                "block_id": "job-description",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": "Development"
            },
            {
                "group_instance": 0,
                "answer_id": "employers-business-answer",
                "block_id": "employers-business",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": "Civil Servant"
            },
            {
                "group_instance": 0,
                "answer_id": "main-job-type-answer",
                "block_id": "main-job-type",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": "Employed by an organisation or business"
            },
            {
                "group_instance": 0,
                "answer_id": "business-name-answer",
                "block_id": "business-name",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": "ONS"
            },
            {
                "group_instance": 1,
                "answer_id": "details-correct-answer",
                "block_id": "details-correct",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": "Yes, this is my full name"
            },
            {
                "group_instance": 1,
                "answer_id": "over-16-answer",
                "block_id": "over-16",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": "Yes"
            },
            {
                "group_instance": 1,
                "answer_id": "private-response-answer",
                "block_id": "private-response",
                "group_id": "household-member",
                "answer_instance": 0,
                "value": "Yes, I want to request a personal form"
            },
            {
                "group_instance": 0,
                "answer_id": "visitor-first-name",
                "block_id": "visitor-name",
                "group_id": "visitors",
                "answer_instance": 0,
                "value": "Diya"
            },
            {
                "group_instance": 0,
                "answer_id": "visitor-last-name",
                "block_id": "visitor-name",
                "group_id": "visitors",
                "answer_instance": 0,
                "value": "K"
            },
            {
                "group_instance": 0,
                "answer_id": "visitor-sex-answer",
                "block_id": "visitor-sex",
                "group_id": "visitors",
                "answer_instance": 0,
                "value": "Female"
            },
            {
                "group_instance": 0,
                "answer_id": "visitor-date-of-birth-answer",
                "block_id": "visitor-date-of-birth",
                "group_id": "visitors",
                "answer_instance": 0,
                "value": "04/11/2016"
            },
            {
                "group_instance": 0,
                "answer_id": "visitor-uk-resident-answer-other",
                "block_id": "visitor-uk-resident",
                "group_id": "visitors",
                "answer_instance": 0,
                "value": ""
            },
            {
                "group_instance": 0,
                "answer_id": "visitor-uk-resident-answer",
                "block_id": "visitor-uk-resident",
                "group_id": "visitors",
                "answer_instance": 0,
                "value": "Yes, usually lives in the United Kingdom"
            },
            {
                "group_instance": 0,
                "answer_id": "visitor-address-answer-postcode",
                "block_id": "visitor-address",
                "group_id": "visitors",
                "answer_instance": 0,
                "value": "530003"
            },
            {
                "group_instance": 0,
                "answer_id": "visitor-address-answer-street",
                "block_id": "visitor-address",
                "group_id": "visitors",
                "answer_instance": 0,
                "value": ""
            },
            {
                "group_instance": 0,
                "answer_id": "visitor-address-answer-building",
                "block_id": "visitor-address",
                "group_id": "visitors",
                "answer_instance": 0,
                "value": "309"
            },
            {
                "group_instance": 0,
                "answer_id": "visitor-address-answer-city",
                "block_id": "visitor-address",
                "group_id": "visitors",
                "answer_instance": 0,
                "value": "Vizag"
            },
            {
                "group_instance": 0,
                "answer_id": "visitor-address-answer-county",
                "block_id": "visitor-address",
                "group_id": "visitors",
                "answer_instance": 0,
                "value": ""
            },
            {
                "group_instance": 1,
                "answer_id": "visitor-first-name",
                "block_id": "visitor-name",
                "group_id": "visitors",
                "answer_instance": 0,
                "value": "Niki"
            },
            {
                "group_instance": 1,
                "answer_id": "visitor-last-name",
                "block_id": "visitor-name",
                "group_id": "visitors",
                "answer_instance": 0,
                "value": "K"
            },
            {
                "group_instance": 1,
                "answer_id": "visitor-sex-answer",
                "block_id": "visitor-sex",
                "group_id": "visitors",
                "answer_instance": 0,
                "value": "Male"
            },
            {
                "group_instance": 1,
                "answer_id": "visitor-date-of-birth-answer",
                "block_id": "visitor-date-of-birth",
                "group_id": "visitors",
                "answer_instance": 0,
                "value": "17/10/1985"
            },
            {
                "group_instance": 1,
                "answer_id": "visitor-uk-resident-answer-other",
                "block_id": "visitor-uk-resident",
                "group_id": "visitors",
                "answer_instance": 0,
                "value": ""
            },
            {
                "group_instance": 1,
                "answer_id": "visitor-uk-resident-answer",
                "block_id": "visitor-uk-resident",
                "group_id": "visitors",
                "answer_instance": 0,
                "value": "Yes, usually lives in the United Kingdom"
            },
            {
                "group_instance": 1,
                "answer_id": "visitor-address-answer-postcode",
                "block_id": "visitor-address",
                "group_id": "visitors",
                "answer_instance": 0,
                "value": "12345"
            },
            {
                "group_instance": 1,
                "answer_id": "visitor-address-answer-street",
                "block_id": "visitor-address",
                "group_id": "visitors",
                "answer_instance": 0,
                "value": ""
            },
            {
                "group_instance": 1,
                "answer_id": "visitor-address-answer-building",
                "block_id": "visitor-address",
                "group_id": "visitors",
                "answer_instance": 0,
                "value": "1009"
            },
            {
                "group_instance": 1,
                "answer_id": "visitor-address-answer-city",
                "block_id": "visitor-address",
                "group_id": "visitors",
                "answer_instance": 0,
                "value": "Detroit"
            },
            {
                "group_instance": 1,
                "answer_id": "visitor-address-answer-county",
                "block_id": "visitor-address",
                "group_id": "visitors",
                "answer_instance": 0,
                "value": ""
            }
        ]

        return expected_downstream_data

    def complete_survey(self, eq_id, form_type_id):
        variant_flags = {'sexual_identity': 'false'}
        self.launchSurvey(eq_id, form_type_id, region_code='GB-ENG', variant_flags=variant_flags, roles=['dumper'])

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

        self.assertInPage('The next section covers questions for Visitor 2')
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

        # Completed Individual section questions for person 1
        self.assertInPage('There are no more questions for Danny Boje')
        self.post(action='save_continue')
        self.assertInPage('The next section covers individual questions for Anjali Yo')
        self.post(action='save_continue')

    def complete_individual_section_person_2(self):
        # Start of Individual section questions for Person 2
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
        self.assertInPage('The next section covers questions for Visitor 1')
        self.post(action='save_continue')

    def complete_household_and_accommodation_section(self):
        # Start of Household and Accommodation section
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
                'central-heating-answer': ['No central heating',
                                           'Gas',
                                           'Electric (including storage heaters)',
                                           'Oil',
                                           'Solid fuel (for example wood, coal)',
                                           'Other central heating']
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
        self.assertInPage('The next section covers individual questions for Danny Boje')
        self.post(action='save_continue')

    def complete_who_lives_here_section(self):
        # We are in the questionnaire
        self.assertInPage('Who lives here?')
        self.assertInPage('>Save and continue<')
        # In Who lives here? Section

        self.post(post_data={'permanent-or-family-home-answer': ['Yes']})
        self.post(action='add_answer')
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
