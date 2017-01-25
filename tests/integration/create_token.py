from app.views.dev_mode import generate_token, create_payload

PAYLOAD = {
    'user': "mci-integration-test",
    "period_str": "April 2016",
    "period_id": "201604",
    "collection_exercise_sid": "789",
    "ru_ref": "123456789012A",
    "ru_name": "MCI Integration Testing",
    "ref_p_start_date": "2016-04-01",
    "ref_p_end_date": "2016-04-30",
    "return_by": "2016-05-06",
    "trad_as": "Integration Tests",
    "employment_date": "1983-06-02",
    "variant_flags": None,
    "exp_time": 3600  # one hour from now
}


def create_token(form_type_id, eq_id, start_date=None, end_date=None, employment_date=None, region_code=None, language_code=None):

    payload_vars = PAYLOAD
    payload_vars['ref_p_start_date'] = start_date or payload_vars['ref_p_start_date']
    payload_vars['ref_p_end_date'] = end_date or payload_vars['ref_p_end_date']
    payload_vars['employment_date'] = employment_date or payload_vars['employment_date']
    payload_vars['eq_id'] = eq_id
    payload_vars['form_type'] = form_type_id
    payload_vars['region_code'] = region_code
    payload_vars['language_code'] = language_code

    payload = create_payload(**payload_vars)

    return generate_token(payload)
