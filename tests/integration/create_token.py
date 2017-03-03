import time
from uuid import uuid4

from app.views.dev_mode import generate_token

PAYLOAD = {
    'user_id': "mci-integration-test",
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
    "region_code": None,
    "language_code": None
}


def create_token(form_type_id, eq_id, **extra_payload):
    payload_vars = PAYLOAD
    payload_vars['eq_id'] = eq_id
    payload_vars['form_type'] = form_type_id
    payload_vars['jti'] = str(uuid4())
    payload_vars['iat'] = time.time()
    payload_vars['exp'] = payload_vars['iat'] + float(3600)  # one hour from now
    for key, value in extra_payload.items():
        payload_vars[key] = value

    return generate_token(payload_vars)
