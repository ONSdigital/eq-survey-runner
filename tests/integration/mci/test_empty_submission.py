import unittest
from app import create_app
from app.dev_mode.views import generate_token, create_payload

# Set up some constants
USER = "mci-integration-test"
EQ_ID = "1"
FORM_TYPE = "0205"
PERIOD_STR = "April 2016"
PERIOD_ID = "201604"
COLLECTION_EXERCISE_SID = "789"
RU_REF = "123456789012A"
RU_NAME = "MCI Integration Testing"
REF_P_START_DATE = "2016-04-01"
REF_P_END_DATE = "2016-04-30"
RETURN_BY = "2016-05-06"
TRAD_AS = "Happy Path Testing"


class TestEmptySubmission(unittest.TestCase):

    def setUp(self):
        self.application = create_app('development')
        self.client = self.application.test_client()

    def test_empty_submission(self):
        # Get a token
        token = self._create_token()
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=True)
        self.assertEquals(resp.status_code, 200)

        # We are on the landing page
        content = resp.get_data(True)
        self.assertRegexpMatches(content, '>Get Started<')

        # We proceed to the questionnaire
        resp = self.client.get('/questionnaire', follow_redirects=True)
        self.assertEquals(resp.status_code, 200)

        # We are in the Questionnaire
        content = resp.get_data(True)
        self.assertRegexpMatches(content, "What are the dates of the sales period you are reporting for\?")
        self.assertRegexpMatches(content, ">Save &amp; Continue<")

        form_data = {
            # Start Date
            "6fd644b0-798e-4a58-a393-a438b32fe637-day": "01",
            "6fd644b0-798e-4a58-a393-a438b32fe637-month": "1",
            "6fd644b0-798e-4a58-a393-a438b32fe637-year": "",
            # End Date
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-day": "01",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-month": "01",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-year": "",
            # Total Turnover
            "e81adc6d-6fb0-4155-969c-d0d646f15345": "100000"
        }

        # We submit the form without a year in the date
        resp = self.client.post('/questionnaire', data=form_data, follow_redirects=True)
        self.assertEquals(resp.status_code, 200)
        content = resp.get_data(True)
        self.assertRegexpMatches(content, "The date entered is not valid.  Please correct your answer.")

        form_data = {
            # Start Date
            "6fd644b0-798e-4a58-a393-a438b32fe637-day": "01",
            "6fd644b0-798e-4a58-a393-a438b32fe637-month": "1",
            "6fd644b0-798e-4a58-a393-a438b32fe637-year": "2016",
            # End Date
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-day": "01",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-month": "01",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-year": "2016",
            # Total Turnover
            "e81adc6d-6fb0-4155-969c-d0d646f15345": ""
        }

        # We submit the form without a turnover value
        resp = self.client.post('/questionnaire', data=form_data, follow_redirects=True)
        self.assertEquals(resp.status_code, 200)
        content = resp.get_data(True)
        self.assertRegexpMatches(content, "Please provide a value, even if your value is 0.")

        form_data = {
            # Start Date
            "6fd644b0-798e-4a58-a393-a438b32fe637-day": "01",
            "6fd644b0-798e-4a58-a393-a438b32fe637-month": "1",
            "6fd644b0-798e-4a58-a393-a438b32fe637-year": "2016",
            # End Date
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-day": "01",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-month": "01",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-year": "2016",
            # Total Turnover
            "e81adc6d-6fb0-4155-969c-d0d646f15345": "rubbish"
        }

        # We submit the form without a invalid turnover value
        resp = self.client.post('/questionnaire', data=form_data, follow_redirects=True)
        self.assertEquals(resp.status_code, 200)
        content = resp.get_data(True)
        self.assertRegexpMatches(content, "Please only enter whole numbers into the field.")

        # Try to access the submission page without correction
        resp = self.client.get('/submission', follow_redirects=True)
        self.assertEquals(resp.status_code, 200)
        content = resp.get_data(True)
        self.assertRegexpMatches(content, "What are the dates of the sales period you are reporting for\?")

    def _create_token(self):
        user = USER
        exp_time = 3600                         # one hour from now
        eq_id = EQ_ID
        period_str = PERIOD_STR
        period_id = PERIOD_ID
        form_type = FORM_TYPE
        collection_exercise_sid = COLLECTION_EXERCISE_SID
        ref_p_start_date = REF_P_START_DATE
        ref_p_end_date = REF_P_END_DATE
        ru_ref = RU_REF
        ru_name = RU_NAME
        trad_as = TRAD_AS
        return_by = RETURN_BY

        payload = create_payload(user, exp_time, eq_id, period_str, period_id,
                                 form_type, collection_exercise_sid, ref_p_start_date,
                                 ref_p_end_date, ru_ref, ru_name, trad_as, return_by)

        return generate_token(payload)
