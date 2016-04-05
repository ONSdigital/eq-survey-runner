import unittest

from app import settings
from app.authentication.invalid_token_exception import InvalidTokenException
from app.authentication.jwt_decoder import Decoder
from app.authentication.no_token_exception import NoTokenException
from tests.app.authentication import TEST_DO_NOT_USE_RRM_PUBLIC_PEM, TEST_DO_NOT_USE_SR_PRIVATE_PEM
from tests.app.authentication import VALID_JWT, VALID_SIGNED_JWT, VALID_JWE


class JWTDecodeTest(unittest.TestCase):
    def setUp(self):
        settings.EQ_SR_PRIVATE_KEY = TEST_DO_NOT_USE_SR_PRIVATE_PEM
        settings.EQ_RRM_PUBLIC_KEY = TEST_DO_NOT_USE_RRM_PUBLIC_PEM
        settings.EQ_SR_PRIVATE_KEY_PASSWORD = "digitaleq"

    def test_decode(self):
        decoder = Decoder()
        token = decoder.decode_jwt_token(VALID_JWT)
        self.assertEquals("jimmy", token.get("user"))

    def test_decode_with_no_token(self):
        decoder = Decoder()
        self.assertRaises(NoTokenException, decoder.decode_jwt_token, None)

    def test_decode_with_invalid_token(self):
        decoder = Decoder()
        token = "asdasdasdasd"
        self.assertRaises(InvalidTokenException, decoder.decode_jwt_token, token)

    def test_decode_signed_jwt_token(self):
        decoder = Decoder()
        token = decoder.decode_signed_jwt_token(VALID_SIGNED_JWT)
        self.assertEquals("jimmy", token.get("user"))

    def test_decode_signed_jwt_token_with_no_token(self):
        decoder = Decoder()
        self.assertRaises(NoTokenException, decoder.decode_signed_jwt_token, None)

    def test_decode_signed_jwt_token_with_invalid_token(self):
        decoder = Decoder()
        token = "asdasdasdasd"
        self.assertRaises(InvalidTokenException, decoder.decode_signed_jwt_token, token)

    def test_decrypt_jwt_token(self):
        decoder = Decoder()
        token = decoder.decrypt_jwt_token(VALID_JWE)
        self.assertEquals("jimmy", token.get("user"))

    def test_decrypt_jwt_token_with_no_token(self):
        decoder = Decoder()
        self.assertRaises(NoTokenException, decoder.decrypt_jwt_token, None)

    def test_decrypt_jwt_token_with_invalid_token(self):
        decoder = Decoder()
        token = "asdasdasdasd"
        self.assertRaises(InvalidTokenException, decoder.decrypt_jwt_token, token)


if __name__ == '__main__':
    unittest.main()
