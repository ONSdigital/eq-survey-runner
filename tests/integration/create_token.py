import time
from uuid import uuid4

from app.cryptography.token_helper import encode_jwt, encrypt_jwe
from app.secrets import KEY_PURPOSE_AUTHENTICATION

PAYLOAD = {
    'user_id': 'integration-test',
    'period_str': 'April 2016',
    'period_id': '201604',
    'collection_exercise_sid': '789',
    'ru_ref': '123456789012A',
    'ru_name': 'Integration Testing',
    'ref_p_start_date': '2016-04-01',
    'ref_p_end_date': '2016-04-30',
    'return_by': '2016-05-06',
    'trad_as': 'Integration Tests',
    'employment_date': '1983-06-02',
    'variant_flags': None,
    'region_code': 'GB-ENG',
    'language_code': 'en',
    'roles': [],
}


class TokenGenerator:

    def __init__(self, secret_store, upstream_kid, sr_public_kid):
        self._secret_store = secret_store
        self._upstream_kid = upstream_kid
        self._sr_public_kid = sr_public_kid

    def create_token(self, form_type_id, eq_id, **extra_payload):
        payload_vars = PAYLOAD.copy()
        payload_vars['eq_id'] = eq_id
        payload_vars['form_type'] = form_type_id
        payload_vars['jti'] = str(uuid4())
        payload_vars['iat'] = time.time()
        payload_vars['exp'] = payload_vars['iat'] + float(3600)  # one hour from now
        for key, value in extra_payload.items():
            payload_vars[key] = value

        return self.generate_token(payload_vars)

    def create_token_without_jti(self, form_type_id, eq_id, **extra_payload):
        payload_vars = PAYLOAD.copy()
        payload_vars['eq_id'] = eq_id
        payload_vars['form_type'] = form_type_id
        payload_vars['iat'] = time.time()
        payload_vars['exp'] = payload_vars['iat'] + float(3600)  # one hour from now
        for key, value in extra_payload.items():
            payload_vars[key] = value

        return self.generate_token(payload_vars)

    def generate_token(self, payload):
        token = encode_jwt(payload, self._upstream_kid, self._secret_store, KEY_PURPOSE_AUTHENTICATION)

        return encrypt_jwe(token, self._sr_public_kid, self._secret_store, KEY_PURPOSE_AUTHENTICATION)
