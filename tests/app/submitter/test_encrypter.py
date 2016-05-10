from cryptography.hazmat.backends.openssl.backend import backend
from cryptography.hazmat.primitives import serialization
from app.submitter.encrypter import Encrypter
from app.cryptography.jwe_decryption import JWERSAOAEPDecryptor
from tests.app.submitter import TEST_DO_NOT_USE_SDX_PRIVATE_KEY, TEST_DO_NOT_USE_SR_PUBLIC_ENCRYPTION_KEY
import jwt
import json
import unittest

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


class Decrypter(JWERSAOAEPDecryptor):

    def __init__(self):
        super().__init__(TEST_DO_NOT_USE_SDX_PRIVATE_KEY)
        self.rrm_public_key = serialization.load_pem_public_key(
              TEST_DO_NOT_USE_SR_PUBLIC_ENCRYPTION_KEY.encode(),
              backend=backend
        )

    def decrypt(self, token):
        signed_token = super().decrypt(token)
        return jwt.decode(signed_token, self.rrm_public_key, algorithms=['RS256'])


class TestEncrypter(unittest.TestCase):
    def test_encrypt(self):
        encrypter = Encrypter()
        encrypted_data = encrypter.encrypt(SUBMISSION_DATA)

        decrypter = Decrypter()
        unencrypted_data = decrypter.decrypt(encrypted_data)

        self.assertEquals(SUBMISSION_DATA["type"], unencrypted_data["type"])
        self.assertEquals(SUBMISSION_DATA["version"], unencrypted_data["version"])
        self.assertEquals(SUBMISSION_DATA["origin"], unencrypted_data["origin"])
        self.assertEquals(SUBMISSION_DATA["survey_id"], unencrypted_data["survey_id"])
        self.assertEquals(SUBMISSION_DATA["collection"], unencrypted_data["collection"])
        self.assertEquals(SUBMISSION_DATA["metadata"], unencrypted_data["metadata"])
        self.assertEquals(SUBMISSION_DATA["paradata"], unencrypted_data["paradata"])
        self.assertEquals(SUBMISSION_DATA["data"], unencrypted_data["data"])
