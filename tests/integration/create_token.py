from app.dev_mode.views import generate_token, create_payload

# Set up some constants
USER = "mci-integration-test"
EQ_ID = "1"
PERIOD_STR = "April 2016"
PERIOD_ID = "201604"
COLLECTION_EXERCISE_SID = "789"
RU_REF = "123456789012A"
RU_NAME = "MCI Integration Testing"
REF_P_START_DATE = "2016-04-01"
REF_P_END_DATE = "2016-04-30"
RETURN_BY = "2016-05-06"
TRAD_AS = "Integration Tests"

def create_token(form_type_id):
        user = USER
        exp_time = 3600                         # one hour from now
        eq_id = EQ_ID
        period_str = PERIOD_STR
        period_id = PERIOD_ID
        form_type = form_type_id
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
