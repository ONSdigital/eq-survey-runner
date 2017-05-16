from tests.integration.integration_test_case import IntegrationTestCase


class TestUkisSubmissionData(IntegrationTestCase):

    def test_ukis_data_matches_expected_1_0001(self):
        self.complete_survey('1', '0001')

        # And the JSON response contains the data I submitted
        actual_downstream_data = self.dumpSubmission()

        tx_id = actual_downstream_data['submission']['tx_id']
        submitted_at = actual_downstream_data['submission']['submitted_at']

        # Enable full dictionary diffs on test failure
        self.maxDiff = None
        self.assertDictEqual(actual_downstream_data, self.get_expected_submission_data(tx_id, submitted_at))

    @staticmethod
    def get_expected_submission_data(tx_id, submitted_at):
        expected_downstream_data = {
            "submission": {
                "data": {
                    "1010": "This business or enterprise group",
                    "1020": "This business with other businesses or organisations",
                    "1030": "Other businesses or organisations",
                    "1100": "Yes",
                    "1210": "High",
                    "1211": "Medium",
                    "1212": "Low",
                    "1213": "Medium",
                    "1220": "Low",
                    "1230": "Not Important",
                    "1250": "Not Important",
                    "1260": "Medium",
                    "1270": "High",
                    "1280": "High",
                    "1290": "Low",
                    "1310": "Yes",
                    "1320": "Yes",
                    "1331": "Advanced machinery and equipment",
                    "1332": "Computer hardware",
                    "1333": "Computer software",
                    "1340": "Yes",
                    "1350": "Yes",
                    "1360": "Yes",
                    "1371": "Changes to product or service design",
                    "1372": "Market research",
                    "1373": "Changes to marketing methods",
                    "1374": "Launch advertising",
                    "1410": "2000",
                    "1420": "1000",
                    "1430": "1500",
                    "1440": "3500",
                    "1450": "5500",
                    "1460": "6500",
                    "1470": "7500",
                    "1510": "Yes",
                    "1520": "Yes",
                    "1530": "No",
                    "1601": "High",
                    "1610": "Low",
                    "1611": "Medium",
                    "1620": "Medium",
                    "1631": "Low",
                    "1632": "Not Important",
                    "1650": "Not Important",
                    "1660": "Low",
                    "1670": "Medium",
                    "1680": "High",
                    "1690": "High",
                    "1821": "UK Regional",
                    "1822": "UK National",
                    "1823": "European Countries",
                    "1851": "UK Regional",
                    "1852": "UK National",
                    "1853": "European Countries",
                    "1854": "Other Countries",
                    "1861": "UK Regional",
                    "1862": "UK National",
                    "1863": "European Countries",
                    "1871": "UK Regional",
                    "1872": "UK National",
                    "1881": "UK Regional",
                    "1882": "UK National",
                    "1891": "UK Regional",
                    "2310": "Yes",
                    "2320": "No",
                    "2330": "Yes",
                    "2340": "No",
                    "2410": "3500",
                    "2420": "4500",
                    "2440": "5500",
                    "2510": "100",
                    "2520": "120",
                    "2610": "90",
                    "2620": "85",
                    "2632": "Design of objects or services",
                    "2636": "Mathematics, statistics",
                    "2650": "None",
                    "2651": "Less than 40%",
                    "2652": "40-90%",
                    "2653": "Over 90%",
                    "2655": "None",
                    "2656": "Less than 40%",
                    "2657": "High",
                    "2658": "Medium",
                    "2659": "Low",
                    "2660": "Not Important",
                    "2661": "Not Important",
                    "2662": "Low",
                    "2663": "Medium",
                    "2664": "High",
                    "2665": "High",
                    "2666": "Medium",
                    "2667": "Low",
                    "2668": "Yes",
                    "2669": "No",
                    "2670": "Yes",
                    "2675": "2014",
                    "2676": "2015",
                    "2677": "2016",
                    "2678": "Not Important",
                    "2700": "Downstream data coverage test",
                    "2800": "23",
                    "2801": "50",
                    "2900": "Yes",
                    "10000": "Yes",
                    "10001": "Yes",
                    "0240": "All other countries",
                    "0430": "Yes",
                    "0601": "This business or enterprise group",
                    "0820": "25",
                    "0230": "European countries",
                    "0602": "This business with other businesses or organisations",
                    "0520": "Yes",
                    "0220": "UK national",
                    "0720": "Yes",
                    "0510": "Yes",
                    "0840": "24",
                    "0830": "25",
                    "0810": "25",
                    "0610": "This business or enterprise group",
                    "0900": "Yes",
                    "0620": "This business with other businesses or organisations",
                    "0603": "Other businesses or organisations",
                    "0710": "Yes",
                    "0410": "Yes",
                    "0420": "No",
                    "0630": "Other businesses or organisations",
                    "0210": "UK regional within approximately 100 miles of this business"
                },
                "origin": "uk.gov.ons.edc.eq",
                "submitted_at": submitted_at,
                "version": "0.0.1",
                "survey_id": "144",
                "flushed": False,
                "collection": {
                    "instrument_id": "0001",
                    "period": "201604",
                    "exercise_sid": "789"
                },
                "metadata": {
                    "ru_ref": "123456789012A",
                    "user_id": "integration-test"
                },
                "type": "uk.gov.ons.edc.eq:surveyresponse",
                "tx_id": tx_id
            }
        }
        return expected_downstream_data

    def complete_survey(self, eq_id, form_type_id):
        self.launchSurvey(eq_id, form_type_id, roles=['dumper'])

        self.landing_page()

        self.general_business_information_section()

        self.business_strategy_and_practices_section()

        self.innovation_investment_section()

        self.goods_and_services_innovation_section()

        self.process_innovation_section()

        self.constraints_on_innovation_section()

        self.factors_affecting_innovation_section()

        self.information_needed_for_innovation_section()

        self.cooperation_on_innovation_section()

        self.public_financial_support_for_innovation_section()

        self.turnover_and_exports_section()

        self.employees_and_skills_section()

        self.general_information_section()

        self.assertInPage('You are now ready to submit this survey')

    def landing_page(self):

        # We are on the landing page

        self.assertInPage('>Start survey<')
        self.assertInPage('UK Innovation Survey')

        # We proceed to the questionnaire

        self.post(action='start_questionnaire')

    def general_information_section(self):

        # We are in General Information section

        self.assertInPage('General Information')
        self.assertInPage('>Save and continue<')
        self.post(post_data={'additional-comments-answer': 'Downstream data coverage test'})
        self.post(post_data={'general-information-hours-answer': '50',
                             'how-long-minutes-answer': '23'})
        self.post(post_data={'approached-telephone-answer': 'Yes'})

    def employees_and_skills_section(self):

        # We are in Employees and Skills section

        self.assertInPage('Employees and Skills')
        self.assertInPage('>Save and continue<')
        self.post(post_data={'employees-2014-answer': '100'})
        self.post(post_data={'employees-2016-answer': '120'})
        self.post(post_data={'employees-qualifications-2016-science-answer': '90',
                             'employees-qualifications-other-2016-answer': '85'})
        form_data = {'employees-in-house-skills-answer': ['Design of objects or services',
                                                          'Mathematics,'
                                                          ' statistics']}
        self.post(form_data)

        # We have completed Employees and Skills section

        self.assertInPage('>Employees and Skills</')
        self.assertInPage('You have successfully completed this section')
        self.post(action='save_continue')

    def turnover_and_exports_section(self):

        # We are in Turnover and Exports section

        self.assertInPage('Turnover and Exports')
        self.assertInPage('>Save and continue<')
        self.post(post_data={'turnover-2014-answer': '3500'})
        self.post(post_data={'turnover-2016-answer': '4500'})
        self.post(post_data={'exports-2016-answer': '5500'})

        # We have completed Turnover and Exports section
        self.assertInPage('>Turnover and Exports</')
        self.assertInPage('You have successfully completed this section')
        self.post(action='save_continue')

    def public_financial_support_for_innovation_section(self):

        # We are in Public Financial Support for Innovation section

        self.assertInPage('Public Financial Support for Innovation')
        self.assertInPage('>Save and continue<')
        self.post(post_data={'public-financial-support-authorities-answer': 'Yes',
                             'public-financial-support-central-government-answer': 'No',
                             'public-financial-support-eu-answer': 'Yes'})

        # We have completed Public Financial Support for Innovation section

        self.assertInPage('>Public Financial Support for Innovation</')
        self.assertInPage('You have successfully completed this section')
        self.post(action='save_continue')

    def cooperation_on_innovation_section(self):

        # We are in Co-operation on Innovation section

        self.assertInPage('Co-operation on Innovation')
        self.assertInPage('>Save and continue<')
        form_data = {'years-internal-investment-r-d-answer': ['UK Regional',
                                                              'UK National',
                                                              'European Countries',
                                                              'Other Countries']}
        self.post(form_data)
        form_data = {'co-operation-suppliers-answer': ['UK Regional',
                                                       'UK National',
                                                       'European Countries']}
        self.post(form_data)
        form_data = {'co-operation-private-sector-answer': ['UK Regional',
                                                            'UK National']}
        self.post(form_data)
        form_data = {'co-operation-public-sector-answer': ['UK Regional']}
        self.post(form_data)
        self.post(action='save_continue')
        form_data = {'co-operation-consultants-answer': ['UK Regional',
                                                         'UK National',
                                                         'European Countries',
                                                         'Other Countries']}
        self.post(form_data)
        form_data = {'co-operation-institutions-answer': ['UK Regional',
                                                          'UK National',
                                                          'European Countries']}
        self.post(form_data)
        form_data = {'co-operation-government-answer': ['UK Regional',
                                                        'UK National']}
        self.post(form_data)
        self.post(post_data={'innovations-protected-patents-answer': 'None'})
        self.post(post_data={'innovations-protected-design-answer': 'Less than 40%'})
        self.post(post_data={'innovations-protected-copyright-answer': '40-90%'})
        self.post(post_data={'innovations-protected-trademark-answer': 'Over 90%'})
        self.post(action='save_continue')
        self.post(post_data={'innovations-protected-services-answer': 'None'})
        self.post(post_data={'innovations-protected-secrecy-answer': 'Less than 40%'})

        # We have completed Co-operation on Innovation section

        self.assertInPage('>Co-operation on Innovation</')
        self.assertInPage('You have successfully completed this section')
        self.post(action='save_continue')

    def information_needed_for_innovation_section(self):

        # We are in Information Needed for Innovation section

        self.assertInPage('Information Needed for Innovation')
        self.assertInPage('>Save and continue<')
        self.post(post_data={'importances-information-innovation-answer': 'High'})
        self.post(post_data={'importances-information-suppliers-answer': 'Medium'})
        self.post(post_data={'importances-information-client-answer': 'Low'})
        self.post(post_data={'importances-information-public-sector-answer': 'Not Important'})
        self.post(action='save_continue')
        self.post(post_data={'importances-information-consultants-answer': 'Not Important'})
        self.post(post_data={'importances-information-universities-answer': 'Low'})
        self.post(post_data={'importances-information-government-answer': 'Medium'})
        self.post(post_data={'importances-information-conferences-answer': 'High'})
        self.post(post_data={'importances-information-associations-answer': 'Low'})
        self.post(post_data={'importances-information-standards-answer': 'Medium'})
        self.post(post_data={'importances-information-publications-answer': 'High'})

        # We have completed Information Needed for Innovation section
        self.assertInPage('>Information Needed for Innovation</')
        self.assertInPage('You have successfully completed this section')
        self.post(action='save_continue')

    def factors_affecting_innovation_section(self):
        # We are in Factors Affecting Innovation section
        self.assertInPage('Factors Affecting Innovation')
        self.assertInPage('>Save and continue<')
        self.post(post_data={'factors-affecting-increasing-range-answer': 'High'})
        self.post(post_data={'factors-affecting-new-markets-answer': 'Medium'})
        self.post(post_data={'factors-affecting-market-share-answer': 'Low'})
        self.post(post_data={'factors-affecting-quality-answer': 'Not Important'})
        self.post(action='save_continue')
        self.post(post_data={'factors-affecting-capacity-answer': 'Not Important'})
        self.post(post_data={'factors-affecting-value-answer': 'Low'})
        self.post(post_data={'factors-affecting-reducing-cost-answer': 'Medium'})
        self.post(post_data={'factors-affecting-health-safety-answer': 'High'})
        self.post(post_data={'factors-affecting-environmental-answer': 'Low'})
        self.post(post_data={'factors-affecting-replacing-answer': 'Medium'})
        self.post(post_data={'factors-affecting-regulatory-answer': 'High'})
        # We have completed Factors Affecting Innovation section
        self.assertInPage('>Factors Affecting Innovation</')
        self.assertInPage('You have successfully completed this section')
        self.post(action='save_continue')

    def constraints_on_innovation_section(self):

        # We are in Constraints on Innovation section

        self.assertInPage('Constraints on Innovation')
        self.assertInPage('>Save and continue<')
        self.post(post_data={'constraints-innovation-activities-abandoned-answser': 'Yes',
                             'constraints-innovation-activities-scaled-back-answser': 'No',
                             'constraints-innovation-activities-ongoing-2016-answser': 'Yes'})
        self.post(post_data={'constraining-innovation-economic-answer': 'High'})
        self.post(post_data={'constraining-innovation-costs-answer': 'Medium'})
        self.post(post_data={'constraining-innovation-finance-answer': 'Low'})
        self.post(post_data={'constraining-innovation-available-finance-answer': 'Not Important'})
        self.post(post_data={'constraining-innovation-lack-qualified-answer': 'Not Important'})
        self.post(post_data={'constraining-innovation-lack-technology-answer': 'Low'})
        self.post(post_data={'constraining-innovation-lack-information-answer': 'Medium'})
        self.post(post_data={'constraining-innovation-dominated-answer': 'High'})
        self.post(post_data={'constraining-innovation-uncertain-answer': 'High'})
        self.post(post_data={'constraining-innovation-government-answer': 'Medium'})
        self.post(post_data={'constraining-innovation-eu-answer': 'Low'})
        self.post(post_data={'constraining-innovation-referendum-answer': 'Not Important'})

        # We have completed Constraints on Innovation section

        self.assertInPage('>Constraints on Innovation </')
        self.assertInPage('You have successfully completed this section')
        self.post(action='save_continue')

    def process_innovation_section(self):

        # We are in Process Innovation section

        self.assertInPage('Process Innovation')
        self.assertInPage('>Save and continue<')
        self.post(post_data={'process-improved-answer': 'Yes'})
        form_data = {'developed-processes-answer': ['This business or enterprise group',
                                                    'This business with other businesses or organisations',
                                                    'Other businesses or organisations']}
        self.post(form_data)
        self.post(post_data={'improved-processes-answer': 'Yes'})

        # We have completed Process Innovation section

        self.assertInPage('>Process Innovation</')
        self.assertInPage('You have successfully completed this section')
        self.post(action='save_continue')

    def goods_and_services_innovation_section(self):

        # We are in Goods and Services Innovation section

        self.assertInPage('Goods and Services Innovation')
        self.assertInPage('>Save and continue<')
        self.post(post_data={'introducing-significantly-improved-goods-answer': 'Yes'})
        form_data = {'gentity-developed-these-goods-answer': ['This business or enterprise group',
                                                              'This business with other businesses or organisations',
                                                              'Other businesses or organisations']}
        self.post(form_data)
        self.post(post_data={'introduce-significantly-improvement-answer': 'Yes'})
        form_data = {'entity-mainly-developed-these-answer': ['This business or enterprise group',
                                                              'This business with other businesses or organisations',
                                                              'Other businesses or organisations']}
        self.post(form_data)
        self.post(post_data={'new-goods-services-innovations-answer': 'Yes'})
        self.post(post_data={'goods-services-innovations-new-answer': 'Yes'})
        self.post(post_data={'percentage-turnover-2016-market-new-answer': '25',
                             'percentage-turnover-2016-business-new-answer': '25',
                             'percentage-turnover-2016-improvement-answer': '25',
                             'percentage-turnover-2016-modified-answer': '24'})

        # We have completed Goods and Services Innovation section

        self.assertInPage('>Goods and Services Innovation</')
        self.assertInPage('You have successfully completed this section')
        self.post(action='save_continue')

    def innovation_investment_section(self):

        # We are in Innovation Investment section

        self.assertInPage('Innovation Investment')
        self.assertInPage('>Save and continue<')
        self.post(post_data={'internal-investment-r-d-answer': 'Yes'})
        form_data = {'years-internal-investment-r-d-answer': ['2014',
                                                              '2015',
                                                              '2016']}
        self.post(form_data)
        self.post(post_data={'expenditure-internal-investment-r-d-answer': '2000'})
        self.post(post_data={'acquisition-internal-investment-r-d-answer': 'Yes'})
        self.post(post_data={'amount-acquisition-internal-investment-r-d-answer': '1000'})
        self.post(post_data={'investment-advanced-machinery-answer': 'Yes'})
        form_data = {'investment-purposes-innovation-answer': ['Advanced machinery and equipment',
                                                               'Computer hardware',
                                                               'Computer software']}
        self.post(form_data)
        self.post(post_data={'amount-acquisition-advanced-machinery-answer': '1500'})
        self.post(post_data={'investment-existing-knowledge-innovation-answer': 'Yes'})
        self.post(post_data={'expenditure-existing-2016-answer': '3500'})
        self.post(post_data={'investment-training-innovative-answer': 'Yes'})
        self.post(post_data={'expenditure-training-innovative-2016-answer': '5500'})
        self.post(post_data={'investment-design-future-innovation-answer': 'Yes'})
        self.post(post_data={'expenditure-design-2016-answer': '6500'})
        self.post(post_data={'investment-introduction-innovations-answer': 'Yes'})
        form_data = {'investment-purposes-innovation-answer-2': ['Changes to product or service design',
                                                                 'Market research',
                                                                 'Changes to marketing methods',
                                                                 'Launch advertising']}
        self.post(form_data)
        self.post(post_data={'expenditure-introduction-innovations-2016-answer': '7500'})

        # We have completed Innovation Investment section

        self.assertInPage('>Innovation Investment</')
        self.assertInPage('You have successfully completed this section')
        self.post(action='save_continue')

    def business_strategy_and_practices_section(self):

        # We are in Business Strategy and Practices section

        self.assertInPage('Business Strategy and Practices')
        self.assertInPage('>Save and continue<')
        self.post(post_data={'business-changes-business-practices-answer': 'Yes',
                             'business-changes-organising-answer': 'No',
                             'business-changes-external-relationships-answer': 'Yes',
                             'business-changes-answer': 'No'})

        # We have completed Business Strategy and Practices section

        self.assertInPage('>Business Strategy &amp; Practices</')
        self.assertInPage('You have successfully completed this section')
        self.post(action='save_continue')

    def general_business_information_section(self):

        # We are in the Questionnaire & We are in General Business Information section

        self.assertInPage('>UK Innovation Survey</')
        self.assertInPage('General Business Information')
        self.assertInPage('>Save and continue<')

        # In General Business Information section
        form_data = {'geographic-markets-answer': ['UK regional within approximately 100 miles of this business',
                                                   'UK national',
                                                   'European countries',
                                                   'All other countries']}
        self.post(form_data)
        self.post(post_data={'significant-events-established-answer': 'Yes',
                             'significant-events-turnover-increase-answer': 'No',
                             'significant-events-turnover-decrease-answer': 'Yes'})

        # We have completed General Business Information section

        self.assertInPage('>General Business Information</')
        self.assertInPage('You have successfully completed this section')
        self.post(action='save_continue')
