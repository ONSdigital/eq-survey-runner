from tests.integration.integration_test_case import IntegrationTestCase


class TestMwssSubmissionData(IntegrationTestCase):

    def test_mwss_data_matches_expected_1_0005(self):
        self.complete_survey('1', '0005')

        # And the JSON response contains the data I submitted
        actual_downstream_data = self.dumpSubmission()
        tx_id = actual_downstream_data['submission']['tx_id']
        submitted_at = actual_downstream_data['submission']['submitted_at']

        self.assertDictEqual(actual_downstream_data, self.get_expected_submission_data(tx_id, submitted_at))

    @staticmethod
    def get_expected_submission_data(tx_id, submitted_at):
        expected_downstream_data = {
            "submission": {
                "tx_id": tx_id,
                "submitted_at": submitted_at,
                "metadata": {
                    "user_id": "integration-test",
                    "ru_ref": "123456789012A"
                },
                "origin": "uk.gov.ons.edc.eq",
                "version": "0.0.1",
                "type": "uk.gov.ons.edc.eq:surveyresponse",
                "collection": {
                    "period": "201604",
                    "instrument_id": "0005",
                    "exercise_sid": "789"
                },
                "data": {
                    "40": "50",
                    "50": "20",
                    "60": "10",
                    "70": "20",
                    "80": "30",
                    "100": "50",
                    "110": "01/04/2016",
                    "120": "20%",
                    "130": "Calendar monthly",
                    "131": "Four weekly",
                    "132": "Five weekly",
                    "151": "10",
                    "152": "10",
                    "153": "10",
                    "171": "2",
                    "172": "2",
                    "173": "2",
                    "181": "3",
                    "182": "3",
                    "183": "3",
                    "200": "30",
                    "210": "01/04/2016",
                    "220": "20%",
                    "300": "General Comments",
                    "195w4": "Yes",
                    "190w4": "Yes",
                    "196w4": "Yes",
                    "110f": "01/04/2016",
                    "140w4": "10",
                    "197w4": "Yes",
                    "70f": "2",
                    "90f": "Yes",
                    "194w5": "More overtime",
                    "120f": "20%",
                    "220w4": "200%",
                    "97w": "Yes",
                    "93f": "Yes",
                    "210w4": "01/04/2016",
                    "300f": "fortnightly Pay",
                    "192w4": "More temporary staff",
                    "194w4": "Less overtime",
                    "196m": "Yes",
                    "40f": "10",
                    "94w": "More overtime",
                    "197w5": "Yes",
                    "95w": "Yes",
                    "193w5": "Yes",
                    "195w5": "Yes",
                    "196w5": "Yes",
                    "140w5": "10",
                    "191w4": "Yes",
                    "300w5": "five Weekly Pay",
                    "134f": "Fortnightly",
                    "100f": "30",
                    "194m": "More overtime",
                    "190m": "Yes",
                    "96w": "Yes",
                    "192w5": "Fewer temporary staff",
                    "191m": "Yes",
                    "193w4": "Yes",
                    "195m": "Yes",
                    "97f": "Yes",
                    "193m": "Yes",
                    "300m": "calendar-monthly Pay",
                    "300w4": "four Weekly Pay",
                    "192m": "More temporary staff",
                    "197m": "Yes",
                    "191w5": "Yes",
                    "91w": "Yes",
                    "92f": "More temporary staff",
                    "50f": "10",
                    "95f": "Yes",
                    "190w5": "Yes",
                    "133w": "Weekly",
                    "96f": "Yes",
                    "90w": "Yes",
                    "92w": "More temporary staff",
                    "210w5": "01/08/2016",
                    "300w": "Weekly Pay",
                    "94f": "More overtime",
                    "220w5": "100",
                    "93w": "Yes",
                    "140m": "10",
                    "200w5": "10",
                    "200w4": "30",
                    "80f": "3",
                    "60f": "1",
                    "91f": "Yes"
                },
                "survey_id": "134",
                "flushed": False
            }
        }
        return expected_downstream_data

    def complete_survey(self, eq_id, form_type_id):
        self.launchSurvey(eq_id, form_type_id, roles=['dumper'])

        # We are on the landing page
        self.assertInPage('>Start survey<')
        self.assertInPage('Monthly Wages and Salaries Survey')

        # We proceed to the questionnaire
        self.post(action='start_questionnaire')

        # We are in the Questionnaire
        self.assertInPage('>Monthly Wages and Salaries Survey</')
        self.assertInPage('Please indicate how frequently employees are paid:')
        self.assertInPage('>Save and continue<')

        # When I submit an answer
        form_data = {'pay-pattern-frequency-answer': ['Weekly', 'Fortnightly',
                                                      'Calendar monthly', 'Four weekly', 'Five weekly']}

        self.post(form_data)

        # We are in weekly pay section
        self.assertInPage('>Weekly Pay</')
        self.assertInPage('The next section covers Weekly pay.')
        self.post(action='save_continue')

        self.post(post_data={'weekly-pay-paid-employees-answer': '50'})
        self.post(post_data={'weekly-pay-gross-pay-answer': '20'})

        self.post(post_data={'weekly-pay-breakdown-holiday-answer': '10',
                             'weekly-pay-breakdown-arrears-answer': '20',
                             'weekly-pay-breakdown-prp-answer': '30'})

        self.post(post_data={'weekly-pay-significant-changes-paid-employees-answer': ['Yes']})
        self.post(post_data={'weekly-pay-significant-changes-redundancies-answer': ['Yes']})
        self.post(post_data={'weekly-pay-significant-changes-temp-employees-answer': ['More temporary staff']})
        self.post(post_data={'weekly-pay-significant-changes-gross-pay-answer': ['Yes']})
        self.post(post_data={'weekly-pay-significant-changes-overtime-answer': ['More overtime']})
        self.post(post_data={'weekly-pay-significant-changes-pay-rates-answer': ['Yes']})

        form_data = {
            # Percentage increase of pay rate
            'weekly-pay-significant-changes-pay-rates-increase-percent-increase-answer': '50',
            # figures are back dated, from when
            'weekly-pay-significant-changes-pay-rates-increase-date-from-answer-day': '01',
            'weekly-pay-significant-changes-pay-rates-increase-date-from-answer-month': '4',
            'weekly-pay-significant-changes-pay-rates-increase-date-from-answer-year': '2016',
            # percentage or number of weekly paid employees who received this new pay rate?
            'weekly-pay-significant-changes-pay-rates-increase-percent-employees-answer': '20%'
        }

        self.post(form_data)
        self.post(post_data={'weekly-pay-significant-changes-industrial-action-answer': ['Yes']})
        self.post(post_data={'weekly-pay-significant-changes-other-answer': ['Yes']})
        self.post(post_data={'weekly-pay-significant-changes-other-specify-answer': 'Weekly Pay'})

        # We are in fortnightly pay section
        self.assertInPage('>Fortnightly Pay</')
        self.assertInPage('The next section covers Fortnightly Pay.')
        self.post(action='save_continue')

        self.post(post_data={'fortnightly-pay-paid-employees-answer': '10'})
        self.post(post_data={'fortnightly-pay-gross-pay-answer': '10'})

        self.post(post_data={'fortnightly-pay-breakdown-holiday-answer': '1',
                             'fortnightly-pay-breakdown-arrears-answer': '2',
                             'fortnightly-pay-breakdown-prp-answer': '3'})

        self.post(post_data={'fortnightly-pay-significant-changes-paid-employees-answer': ['Yes']})
        self.post(post_data={'fortnightly-pay-significant-changes-redundancies-answer': ['Yes']})
        self.post(post_data={'fortnightly-pay-significant-changes-temp-employees-answer': ['More temporary staff']})
        self.post(post_data={'fortnightly-pay-significant-changes-gross-pay-answer': ['Yes']})
        self.post(post_data={'fortnightly-pay-significant-changes-overtime-answer': ['More overtime']})
        self.post(post_data={'fortnightly-pay-significant-changes-pay-rates-answer': ['Yes']})

        form_data = {
            # Percentage increase of pay rate
            'fortnightly-pay-significant-changes-pay-rates-increase-percent-increase-answer': '30',
            # figures are back dated, from when
            'fortnightly-pay-significant-changes-pay-rates-increase-date-from-answer-day': '01',
            'fortnightly-pay-significant-changes-pay-rates-increase-date-from-answer-month': '4',
            'fortnightly-pay-significant-changes-pay-rates-increase-date-from-answer-year': '2016',
            # percentage or number of fortnightly paid employees who received this new pay rate?
            'fortnightly-pay-significant-changes-pay-rates-increase-percent-employees-answer': '20%'
        }

        self.post(form_data)
        self.post(post_data={'fortnightly-pay-significant-changes-industrial-action-answer': ['Yes']})
        self.post(post_data={'fortnightly-pay-significant-changes-other-answer': ['Yes']})
        self.post(post_data={'fortnightly-pay-significant-changes-other-specify-answer': 'fortnightly Pay'})

        # We are in Calendar Monthly Pay section
        self.assertInPage('>Calendar Monthly Pay</')
        self.assertInPage('The next section covers Calendar Monthly pay.')
        self.post(action='save_continue')

        self.post(post_data={'calendar-monthly-pay-paid-employees-answer': '10'})
        self.post(post_data={'calendar-monthly-pay-gross-pay-answer': '10'})

        self.post(post_data={'calendar-monthly-pay-breakdown-arrears-answer': '2',
                             'calendar-monthly-pay-breakdown-prp-answer': '3'})

        self.post(post_data={'calendar-monthly-pay-significant-changes-paid-employees-answer': ['Yes']})
        self.post(post_data={'calendar-monthly-pay-significant-changes-redundancies-answer': ['Yes']})
        self.post(post_data={'calendar-monthly-pay-significant-changes-temp-employees-answer': ['More temporary staff']})
        self.post(post_data={'calendar-monthly-pay-significant-changes-gross-pay-answer': ['Yes']})
        self.post(post_data={'calendar-monthly-pay-significant-changes-overtime-answer': ['More overtime']})
        self.post(post_data={'calendar-monthly-pay-significant-changes-pay-rates-answer': ['Yes']})

        form_data = {
            # Percentage increase of pay rate
            'calendar-monthly-pay-significant-changes-pay-rates-increase-percent-increase-answer': '30',
            # figures are back dated, from when
            'calendar-monthly-pay-significant-changes-pay-rates-increase-date-from-answer-day': '01',
            'calendar-monthly-pay-significant-changes-pay-rates-increase-date-from-answer-month': '4',
            'calendar-monthly-pay-significant-changes-pay-rates-increase-date-from-answer-year': '2016',
            # percentage or number of calendar-monthly paid employees who received this new pay rate?
            'calendar-monthly-pay-significant-changes-pay-rates-increase-percent-employees-answer': '20%'
        }

        self.post(form_data)
        self.post(post_data={'calendar-monthly-pay-significant-changes-industrial-action-answer': ['Yes']})
        self.post(post_data={'calendar-monthly-pay-significant-changes-other-answer': ['Yes']})
        self.post(post_data={'calendar-monthly-pay-significant-changes-other-specify-answer': 'calendar-monthly Pay'})

        # We are in Four Weekly Pay section
        self.assertInPage('>Four Weekly Pay</')
        self.assertInPage('The next section covers Four Weekly pay.')
        self.post(action='save_continue')

        self.post(post_data={'four-weekly-pay-paid-employees-answer': '10'})
        self.post(post_data={'four-weekly-pay-gross-pay-answer': '10'})

        self.post(post_data={'four-weekly-pay-breakdown-arrears-answer': '2',
                             'four-weekly-pay-breakdown-prp-answer': '3'})

        self.post(post_data={'four-weekly-pay-significant-changes-paid-employees-answer': ['Yes']})
        self.post(post_data={'four-weekly-pay-significant-changes-redundancies-answer': ['Yes']})
        self.post(post_data={'four-weekly-pay-significant-changes-temp-employees-answer': ['More temporary staff']})
        self.post(post_data={'four-weekly-pay-significant-changes-gross-pay-answer': ['Yes']})
        self.post(post_data={'four-weekly-pay-significant-changes-overtime-answer': ['Less overtime']})
        self.post(post_data={'four-weekly-pay-significant-changes-pay-rates-answer': ['Yes']})

        form_data = {
            # Percentage increase of pay rate
            'four-weekly-pay-significant-changes-pay-rates-increase-percent-increase-answer': '30',
            # figures are back dated, from when
            'four-weekly-pay-significant-changes-pay-rates-increase-date-from-answer-day': '01',
            'four-weekly-pay-significant-changes-pay-rates-increase-date-from-answer-month': '4',
            'four-weekly-pay-significant-changes-pay-rates-increase-date-from-answer-year': '2016',
            # percentage or number of four-weekly paid employees who received this new pay rate?
            'four-weekly-pay-significant-changes-pay-rates-increase-percent-employees-answer': '200%'
        }

        self.post(form_data)
        self.post(post_data={'four-weekly-pay-significant-changes-industrial-action-answer': ['Yes']})
        self.post(post_data={'four-weekly-pay-significant-changes-other-answer': ['Yes']})
        self.post(post_data={'four-weekly-pay-significant-changes-other-specify-answer': 'four Weekly Pay'})

        # We are in Five Weekly Pay section
        self.assertInPage('>Five Weekly Pay</')
        self.assertInPage('The next section covers Five Weekly Pay.')
        self.post(action='save_continue')

        self.post(post_data={'five-weekly-pay-paid-employees-answer': '10'})
        self.post(post_data={'five-weekly-pay-gross-pay-answer': '10'})

        self.post(post_data={'five-weekly-pay-breakdown-arrears-answer': '2',
                             'five-weekly-pay-breakdown-prp-answer': '3'})

        self.post(post_data={'five-weekly-pay-significant-changes-paid-employees-answer': ['Yes']})
        self.post(post_data={'five-weekly-pay-significant-changes-redundancies-answer': ['Yes']})
        self.post(post_data={'five-weekly-pay-significant-changes-temp-employees-answer': ['Fewer temporary staff']})
        self.post(post_data={'five-weekly-pay-significant-changes-gross-pay-answer': ['Yes']})
        self.post(post_data={'five-weekly-pay-significant-changes-overtime-answer': ['More overtime']})
        self.post(post_data={'five-weekly-pay-significant-changes-pay-rates-answer': ['Yes']})

        form_data = {
            # Percentage increase of pay rate
            'five-weekly-pay-significant-changes-pay-rates-increase-percent-increase-answer': '10',
            # figures are back dated, from when
            'five-weekly-pay-significant-changes-pay-rates-increase-date-from-answer-day': '01',
            'five-weekly-pay-significant-changes-pay-rates-increase-date-from-answer-month': '8',
            'five-weekly-pay-significant-changes-pay-rates-increase-date-from-answer-year': '2016',
            # percentage or number of five-weekly paid employees who received this new pay rate?
            'five-weekly-pay-significant-changes-pay-rates-increase-percent-employees-answer': '100'
        }

        self.post(form_data)
        self.post(post_data={'five-weekly-pay-significant-changes-industrial-action-answer': ['Yes']})
        self.post(post_data={'five-weekly-pay-significant-changes-other-answer': ['Yes']})
        self.post(post_data={'five-weekly-pay-significant-changes-other-specify-answer': 'five Weekly Pay'})

        # We are in Five Weekly Pay section
        self.assertInPage('>General Comments</')
        self.assertInPage('The next section covers general comments about this survey.')
        self.post(action='save_continue')

        self.post(post_data={'general-comments-answer': 'General Comments'})

        self.assertInUrl('summary')
