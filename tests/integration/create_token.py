from app.dev_mode.views import generate_token, create_payload

# Set up some constants
USER = "mci-integration-test"
PERIOD_STR = "April 2016"
PERIOD_ID = "201604"
COLLECTION_EXERCISE_SID = "789"
RU_REF = "123456789012A"
RU_NAME = "MCI Integration Testing"
REF_P_START_DATE = "2016-04-01"
REF_P_END_DATE = "2016-04-30"
RETURN_BY = "2016-05-06"
TRAD_AS = "Integration Tests"
EMPLOYMENT_P_DATE = "1983-06-02"


def create_token(form_type_id, eq_id, start_date=None, end_date=None, employment_date=None, region_code=None, language_code=None):
    user = USER
    exp_time = 3600                         # one hour from now
    eq_id = eq_id
    period_str = PERIOD_STR
    period_id = PERIOD_ID
    form_type = form_type_id
    collection_exercise_sid = COLLECTION_EXERCISE_SID

    if start_date is None:
        ref_p_start_date = REF_P_START_DATE
    else:
        ref_p_start_date = start_date

    if end_date is None:
        ref_p_end_date = REF_P_END_DATE
    else:
        ref_p_end_date = end_date

    if employment_date is None:
        employment_date = EMPLOYMENT_P_DATE
    else:
        employment_date = employment_date

    ru_ref = RU_REF
    ru_name = RU_NAME
    trad_as = TRAD_AS
    return_by = RETURN_BY
    variant_flags = None

    payload = create_payload(user=user,
                             exp_time=exp_time,
                             eq_id=eq_id,
                             period_str=period_str,
                             period_id=period_id,
                             form_type=form_type,
                             collection_exercise_sid=collection_exercise_sid,
                             ref_p_start_date=ref_p_start_date,
                             ref_p_end_date=ref_p_end_date,
                             ru_ref=ru_ref,
                             ru_name=ru_name,
                             trad_as=trad_as,
                             return_by=return_by,
                             employment_date=employment_date,
                             region_code=region_code,
                             language_code=language_code,
                             variant_flags=variant_flags)

    return generate_token(payload)
