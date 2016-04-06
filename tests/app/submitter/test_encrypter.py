from cryptography.hazmat.backends.openssl.backend import backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from app.submitter.encrypter import Encrypter
from tests.app.submitter import TEST_DO_NOT_USE_SDX_PRIVATE_KEY, TEST_DO_NOT_USE_SR_PUBLIC_ENCRYPTION_KEY
import base64
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


class Decrypter(object):
    def __init__(self):
        self.rrm_public_key = serialization.load_pem_public_key(
            TEST_DO_NOT_USE_SR_PUBLIC_ENCRYPTION_KEY.encode(),
            backend=backend
        )
        self.sr_private_key = serialization.load_pem_private_key(
            TEST_DO_NOT_USE_SDX_PRIVATE_KEY.encode(),
            password=b'digitaleq',
            backend=backend
        )

    def decrypt(self, token):
        tokens = token.split('.')
        if len(tokens) != 5:
            raise ValueError("Incorrect size")
        jwe_protected_header = tokens[0]
        encrypted_key = tokens[1]
        encoded_iv = tokens[2]
        encoded_cipher_text = tokens[3]
        encoded_tag = tokens[4]

        decrypted_key = self._decrypt_key(encrypted_key)
        iv = self._base64_decode(encoded_iv)
        tag = self._base64_decode(encoded_tag)
        cipher_text = self._base64_decode(encoded_cipher_text)

        signed_token = self._decrypt_cipher_text(cipher_text, iv, decrypted_key, tag, jwe_protected_header)
        return jwt.decode(signed_token, self.rrm_public_key, algorithms=['RS256'])

    def _decrypt_key(self, encrypted_key):
        decoded_key = self._base64_decode(encrypted_key)
        key = self.sr_private_key.decrypt(decoded_key, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA1()), algorithm=hashes.SHA1(), label=None))
        return key

    def _decrypt_cipher_text(self, cipher_text, iv, key, tag, jwe_protected_header):
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=backend)
        decryptor = cipher.decryptor()
        decryptor.authenticate_additional_data(jwe_protected_header.encode())
        decrypted_token = decryptor.update(cipher_text) + decryptor.finalize()
        return decrypted_token

    @staticmethod
    def _base64_decode(text):
        # if the text is not a multiple of 4 pad with trailing =
        # some base64 libraries don't pad data but Python is strict
        # and will throw a incorrect padding error if we don't do this
        if len(text) % 4 != 0:
            while len(text) % 4 != 0:
                text += "="
        return base64.urlsafe_b64decode(text)


class TestEncrypter(unittest.TestCase):
    def test_encrypt(self):
        encrypter = Encrypter()
        encrypted_data = encrypter.encrypt(SUBMISSION_DATA)

        decrypter = Decrypter()
        unencrypted_data = decrypter.decrypt(encrypted_data.decode())

        self.assertEquals(SUBMISSION_DATA["type"], unencrypted_data["type"])
        self.assertEquals(SUBMISSION_DATA["version"], unencrypted_data["version"])
        self.assertEquals(SUBMISSION_DATA["origin"], unencrypted_data["origin"])
        self.assertEquals(SUBMISSION_DATA["survey_id"], unencrypted_data["survey_id"])
        self.assertEquals(SUBMISSION_DATA["collection"], unencrypted_data["collection"])
        self.assertEquals(SUBMISSION_DATA["metadata"], unencrypted_data["metadata"])
        self.assertEquals(SUBMISSION_DATA["paradata"], unencrypted_data["paradata"])
        self.assertEquals(SUBMISSION_DATA["data"], unencrypted_data["data"])
