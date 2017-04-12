import unittest

from app.authentication.invalid_token_exception import InvalidTokenException
from app.authentication.jwt_decoder import JWTDecryptor
from app.authentication.no_token_exception import NoTokenException
from tests.app.authentication import TEST_DO_NOT_USE_RRM_PUBLIC_PEM, TEST_DO_NOT_USE_SR_PRIVATE_PEM, TEST_DO_NOT_USE_SR_PRIVATE_PEM_PASSWORD
from tests.app.authentication import VALID_SIGNED_JWT, VALID_JWE


class JWTDecodeTest(unittest.TestCase):
    def setUp(self):
        self.SR_PRIVATE_KEY = TEST_DO_NOT_USE_SR_PRIVATE_PEM
        self.RRM_PUBLIC_KEY = TEST_DO_NOT_USE_RRM_PUBLIC_PEM
        self.SR_PRIVATE_KEY_PASSWORD = TEST_DO_NOT_USE_SR_PRIVATE_PEM_PASSWORD

        self.good_args = (self.SR_PRIVATE_KEY, self.SR_PRIVATE_KEY_PASSWORD, self.RRM_PUBLIC_KEY)

    def test_invalid_keymat_sr_private_key(self):
        with self.assertRaises(OSError) as ose:
            JWTDecryptor(None, self.SR_PRIVATE_KEY_PASSWORD, self.RRM_PUBLIC_KEY)
        self.assertIn("keymat not configured correctly", ose.exception.args)

    def test_invalid_keymat_sr_private_key_password(self):
        with self.assertRaises(OSError) as ose:
            JWTDecryptor(self.SR_PRIVATE_KEY, None, self.RRM_PUBLIC_KEY)
        self.assertIn("keymat not configured correctly", ose.exception.args)

    def test_invalid_keymat_rrm_public_key(self):
        with self.assertRaises(OSError) as ose:
            JWTDecryptor(self.SR_PRIVATE_KEY, self.SR_PRIVATE_KEY_PASSWORD, None)
        self.assertIn("keymat not configured correctly", ose.exception.args)

    def test_decode_signed_jwt_token(self):
        decoder = JWTDecryptor(*self.good_args)
        token = decoder.decode_signed_jwt_token(VALID_SIGNED_JWT, 120)
        self.assertEqual("jimmy", token.get("user"))

    def test_decode_signed_jwt_token_with_no_token(self):
        decoder = JWTDecryptor(*self.good_args)
        self.assertRaises(NoTokenException, decoder.decode_signed_jwt_token, *(None, 120))

    def test_decode_signed_jwt_token_with_invalid_token(self):
        decoder = JWTDecryptor(*self.good_args)
        token = "asdasdasdasd"
        self.assertRaises(InvalidTokenException, decoder.decode_signed_jwt_token, *(token, 120))

    def test_decrypt_jwt_token(self):
        decoder = JWTDecryptor(*self.good_args)
        token = decoder.decrypt_jwt_token(VALID_JWE, 120)
        self.assertEqual("jimmy", token.get("user"))

    def test_decrypt_jwt_token_with_no_token(self):
        decoder = JWTDecryptor(*self.good_args)
        self.assertRaises(NoTokenException, decoder.decrypt_jwt_token, *(None, 120))

    def test_decrypt_jwt_token_with_invalid_token(self):
        decoder = JWTDecryptor(*self.good_args)
        token = "asdasdasdasd"
        self.assertRaises(InvalidTokenException, decoder.decrypt_jwt_token, *(token, 120))


if __name__ == '__main__':
    unittest.main()
