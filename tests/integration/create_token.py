import time
from uuid import uuid4

from sdc.crypto.encrypter import encrypt
from sdc.crypto.jwt_helper import encode

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

    @staticmethod
    def _get_payload_with_params(form_type_id, eq_id, survey_url=None, **extra_payload):
        payload_vars = PAYLOAD.copy()
        payload_vars['eq_id'] = eq_id
        payload_vars['form_type'] = form_type_id
        if survey_url:
            payload_vars['survey_url'] = survey_url
        for key, value in extra_payload.items():
            payload_vars[key] = value

        payload_vars['iat'] = time.time()
        payload_vars['exp'] = payload_vars['iat'] + float(3600)  # one hour from now
        payload_vars['jti'] = str(uuid4())

        return payload_vars

    def create_token(self, form_type_id, eq_id, **extra_payload):
        payload_vars = self._get_payload_with_params(form_type_id, eq_id, None, **extra_payload)

        return self.generate_token(payload_vars)

    def create_token_without_jti(self, form_type_id, eq_id, **extra_payload):
        payload_vars = self._get_payload_with_params(form_type_id, eq_id, None, **extra_payload)
        del payload_vars['jti']

        return self.generate_token(payload_vars)

    def create_token_with_survey_url(self, form_type_id, eq_id, survey_url, **extra_payload):
        payload_vars = self._get_payload_with_params(form_type_id, eq_id, survey_url, **extra_payload)

        return self.generate_token(payload_vars)

    def generate_token(self, payload):
        token = encode(payload, self._upstream_kid, self._secret_store, KEY_PURPOSE_AUTHENTICATION)

        return encrypt(token, self._sr_public_kid, self._secret_store, KEY_PURPOSE_AUTHENTICATION)

    def encode(claims, kid, secret_store, purpose):
        private_jwk = secret_store.get_private_key_by_kid(purpose, kid).as_jwk()

        header = {
            'kid': kid,
            'typ': 'jwt',
            'alg': 'RS256',
        }
        token = jwt.JWT(claims=claims, header=header)

        token.make_signed_token(private_jwk)

        return token.serialize()
