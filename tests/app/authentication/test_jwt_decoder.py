import unittest

from app import settings
from app.authentication.invalid_token_exception import InvalidTokenException
from app.authentication.jwt_decoder import JWTDecryptor
from app.authentication.no_token_exception import NoTokenException
from tests.app.authentication import TEST_DO_NOT_USE_RRM_PUBLIC_PEM, TEST_DO_NOT_USE_SR_PRIVATE_PEM
from tests.app.authentication import VALID_SIGNED_JWT, VALID_JWE


class JWTDecodeTest(unittest.TestCase):
    def setUp(self):
        settings.EQ_USER_AUTHENTICATION_SR_PRIVATE_KEY = TEST_DO_NOT_USE_SR_PRIVATE_PEM
        settings.EQ_USER_AUTHENTICATION_RRM_PUBLIC_KEY = TEST_DO_NOT_USE_RRM_PUBLIC_PEM
        settings.EQ_USER_AUTHENTICATION_SR_PRIVATE_KEY_PASSWORD = "digitaleq"

    def test_invalid_keymat_sr_private_key(self):
        settings.EQ_USER_AUTHENTICATION_SR_PRIVATE_KEY = None
        with self.assertRaises(OSError) as ose:
            JWTDecryptor()
        self.assertIn("KEYMAT not configured correctly.", ose.exception.args)

    def test_invalid_keymat_sr_private_key_password(self):
        settings.EQ_USER_AUTHENTICATION_RRM_PUBLIC_KEY = None
        with self.assertRaises(OSError) as ose:
            JWTDecryptor()
        self.assertIn("KEYMAT not configured correctly.", ose.exception.args)

    def test_invalid_keymat_rrm_public_key(self):
        settings.EQ_USER_AUTHENTICATION_SR_PRIVATE_KEY_PASSWORD = None
        with self.assertRaises(OSError) as ose:
            JWTDecryptor()
        self.assertIn("KEYMAT not configured correctly.", ose.exception.args)

    def test_decode_signed_jwt_token(self):
        decoder = JWTDecryptor()
        token = decoder.decode_signed_jwt_token(VALID_SIGNED_JWT)
        self.assertEquals("jimmy", token.get("user"))

    def test_decode_signed_jwt_token_with_no_token(self):
        decoder = JWTDecryptor()
        self.assertRaises(NoTokenException, decoder.decode_signed_jwt_token, None)

    def test_decode_signed_jwt_token_with_invalid_token(self):
        decoder = JWTDecryptor()
        token = "asdasdasdasd"
        self.assertRaises(InvalidTokenException, decoder.decode_signed_jwt_token, token)

    def test_decrypt_jwt_token(self):
        decoder = JWTDecryptor()
        token = decoder.decrypt_jwt_token(VALID_JWE)
        self.assertEquals("jimmy", token.get("user"))

    def test_decrypt_jwt_token_with_no_token(self):
        decoder = JWTDecryptor()
        self.assertRaises(NoTokenException, decoder.decrypt_jwt_token, None)

    def test_decrypt_jwt_token_with_invalid_token(self):
        decoder = JWTDecryptor()
        token = "asdasdasdasd"
        self.assertRaises(InvalidTokenException, decoder.decrypt_jwt_token, token)


if __name__ == '__main__':
    unittest.main()
