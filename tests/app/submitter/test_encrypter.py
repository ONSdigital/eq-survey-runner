import json
import unittest

from jwcrypto import jwt

from app.cryptography.token_helper import decrypt_jwe, extract_kid_from_header
from app.secrets import SecretStore, KEY_PURPOSE_SUBMISSION
from app.submitter.encrypter import encrypt
from tests.app.submitter import (
    TEST_DO_NOT_USE_SDX_PRIVATE_KEY,
    TEST_DO_NOT_USE_SR_PRIVATE_SIGNING_KEY,
    TEST_DO_NOT_USE_SR_PUBLIC_ENCRYPTION_KEY,
    TEST_DO_NOT_USE_EQ_SUBMISSION_SDX_PUBLIC_KEY
)

SUBMISSION_DATA = json.loads("""
      {
        "type" : "uk.gov.ons.edc.eq:surveyresponse",
        "version" : "0.0.1",
        "origin" : "uk.gov.ons.edc.eq",
        "survey_id": "021",
        "collection":{
          "exercise_sid": "hfjdskf",
          "instrument_id": "yui789",
          "period": "2016-02-01"
        },
        "submitted_at": "2016-03-07T15:28:05Z",
        "metadata": {
          "user_id": "789473423",
          "ru_ref": "432423423423"
        },
        "paradata": {},
        "data": {
          "001": "2016-01-01",
          "002": "2016-03-30"
        }
      }""")


class TestEncrypter(unittest.TestCase):
    def test_encrypt(self):
        secret_store_encrypt = SecretStore({
            "keys": {
                "EQ_SUBMISSION_SDX_PUBLIC_KEY": {'purpose': KEY_PURPOSE_SUBMISSION,
                                                 'type': 'public',
                                                 'value': TEST_DO_NOT_USE_EQ_SUBMISSION_SDX_PUBLIC_KEY},
                "EQ_SUBMISSION_SR_PRIVATE_SIGNING_KEY": {'purpose': KEY_PURPOSE_SUBMISSION,
                                                         'type': 'private',
                                                         'value': TEST_DO_NOT_USE_SR_PRIVATE_SIGNING_KEY},
            }
        })

        secret_store_decrypt = SecretStore({
            "keys": {
                "EQ_SUBMISSION_SDX_PUBLIC_KEY": {'purpose': KEY_PURPOSE_SUBMISSION,
                                                 'type': 'private',
                                                 'value': TEST_DO_NOT_USE_SDX_PRIVATE_KEY},
                "EQ_SUBMISSION_SR_PRIVATE_SIGNING_KEY": {'purpose': KEY_PURPOSE_SUBMISSION,
                                                         'type': 'public',
                                                         'value': TEST_DO_NOT_USE_SR_PUBLIC_ENCRYPTION_KEY},
            }
        })

        encrypted_data = encrypt(SUBMISSION_DATA, secret_store_encrypt)

        signed_token = decrypt_jwe(encrypted_data, secret_store_decrypt, KEY_PURPOSE_SUBMISSION)

        unencrypted_data = decode_jwt(signed_token, secret_store_decrypt)

        self.assertEqual(SUBMISSION_DATA["type"], unencrypted_data["type"])
        self.assertEqual(SUBMISSION_DATA["version"], unencrypted_data["version"])
        self.assertEqual(SUBMISSION_DATA["origin"], unencrypted_data["origin"])
        self.assertEqual(SUBMISSION_DATA["survey_id"], unencrypted_data["survey_id"])
        self.assertEqual(SUBMISSION_DATA["collection"], unencrypted_data["collection"])
        self.assertEqual(SUBMISSION_DATA["metadata"], unencrypted_data["metadata"])
        self.assertEqual(SUBMISSION_DATA["paradata"], unencrypted_data["paradata"])
        self.assertEqual(SUBMISSION_DATA["data"], unencrypted_data["data"])


def decode_jwt(jwt_token, secret_store):
    jwt_kid = extract_kid_from_header(jwt_token)

    public_key = secret_store.get_public_key_by_kid(KEY_PURPOSE_SUBMISSION, jwt_kid)

    signed_token = jwt.JWT(algs=['RS256'], check_claims={})

    signed_token.deserialize(jwt_token, key=public_key.as_jwk())

    return json.loads(signed_token.claims)
