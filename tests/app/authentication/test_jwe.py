import os
import unittest

from app import settings
from app.authentication.invalid_token_exception import InvalidTokenException
from app.authentication.jwt_decoder import JWTDecryptor
from app.dev_mode.jwt_encoder import Encoder
from tests.app.authentication import TEST_DO_NOT_USE_RRM_PUBLIC_PEM, TEST_DO_NOT_USE_SR_PRIVATE_PEM, VALID_SIGNED_JWT, VALID_JWE


class JWETest(unittest.TestCase):
    def setUp(self):
        settings.EQ_USER_AUTHENTICATION_SR_PRIVATE_KEY = TEST_DO_NOT_USE_SR_PRIVATE_PEM
        settings.EQ_USER_AUTHENTICATION_RRM_PUBLIC_KEY = TEST_DO_NOT_USE_RRM_PUBLIC_PEM
        settings.EQ_USER_AUTHENTICATION_SR_PRIVATE_KEY_PASSWORD = "digitaleq"

    def test_valid_jwe(self):
        decoder = JWTDecryptor()
        token = decoder.decrypt_jwt_token(VALID_JWE)
        self.assertEquals("jimmy", token.get("user"))

    def test_does_not_contain_four_instances_of_full_stop(self):
        jwe = VALID_JWE.replace('.', '', 1)
        decoder = JWTDecryptor()
        with self.assertRaises(InvalidTokenException) as ite:
            decoder.decrypt_jwt_token(jwe)
        self.assertIn("Incorrect size", ite.exception.value)

    def test_missing_algorithm(self):
        jwe_protected_header = b'{"enc":"A256GCM"}'
        encoder = Encoder()
        jwe = encoder.encrypt_token(VALID_SIGNED_JWT.encode(), jwe_protected_header=encoder._base_64_encode(jwe_protected_header))

        decoder = JWTDecryptor()
        with self.assertRaises(InvalidTokenException) as ite:
            decoder.decrypt_jwt_token(jwe.decode())
        self.assertIn("Missing Algorithm", ite.exception.value)

    def test_invalid_algorithm(self):
        jwe_protected_header = b'{"alg":"PBES2_HS256_A128KW","enc":"A256GCM"}'
        encoder = Encoder()
        jwe = encoder.encrypt_token(VALID_SIGNED_JWT.encode(), jwe_protected_header=encoder._base_64_encode(jwe_protected_header))

        decoder = JWTDecryptor()
        with self.assertRaises(InvalidTokenException) as ite:
            decoder.decrypt_jwt_token(jwe.decode())
        self.assertIn("Invalid Algorithm", ite.exception.value)

    def test_enc_missing(self):
        jwe_protected_header = b'{"alg":"RSA-OAEP"}'

        encoder = Encoder()
        jwe = encoder.encrypt_token(VALID_SIGNED_JWT.encode(), jwe_protected_header=encoder._base_64_encode(jwe_protected_header))

        decoder = JWTDecryptor()
        with self.assertRaises(InvalidTokenException) as ite:
            decoder.decrypt_jwt_token(jwe.decode())
        self.assertIn("Missing Encoding", ite.exception.value)

    def test_invalid_enc(self):
        jwe_protected_header = b'{"alg":"RSA-OAEP","enc":"A128GCM"}'
        encoder = Encoder()
        jwe = encoder.encrypt_token(VALID_SIGNED_JWT.encode(), jwe_protected_header=encoder._base_64_encode(jwe_protected_header))

        decoder = JWTDecryptor()
        with self.assertRaises(InvalidTokenException) as ite:
            decoder.decrypt_jwt_token(jwe.decode())
        self.assertIn("Invalid Encoding", ite.exception.value)

    def test_jwe_header_contains_alg_twice(self):
        jwe_protected_header = b'{"alg":"RSA-OAEP","alg":"RSA-OAEP","enc":"A256GCM"}'
        encoder = Encoder()
        jwe = encoder.encrypt_token(VALID_SIGNED_JWT.encode(), jwe_protected_header=encoder._base_64_encode(jwe_protected_header))

        decoder = JWTDecryptor()
        with self.assertRaises(InvalidTokenException) as ite:
            decoder.decrypt_jwt_token(jwe.decode())
        self.assertIn("InvalidTag", ite.exception.value)

    def test_jwe_header_only_contains_alg_and_enc(self):
        jwe_protected_header = b'{"alg":"RSA-OAEP","enc":"A256GCM", "test":"test"}'
        encoder = Encoder()
        jwe = encoder.encrypt_token(VALID_SIGNED_JWT.encode(), jwe_protected_header=encoder._base_64_encode(jwe_protected_header))

        decoder = JWTDecryptor()
        with self.assertRaises(InvalidTokenException) as ite:
            decoder.decrypt_jwt_token(jwe.decode())
        self.assertIn("InvalidTag", ite.exception.value)

    def test_jwe_key_not_2048_bits(self):
        cek = os.urandom(32)

        encoder = Encoder()
        encrypted_key = encoder._encrypted_key(cek)
        encrypted_key = encrypted_key[0:len(encrypted_key) - 2]
        jwe = encoder.encrypt_token(VALID_SIGNED_JWT.encode(), cek=cek, encrypted_key=encrypted_key)

        decoder = JWTDecryptor()
        with self.assertRaises(InvalidTokenException) as ite:
            decoder.decrypt_jwt_token(jwe.decode())
        self.assertIn("ValueError", ite.exception.value)

    def test_cek_not_256_bits(self):
        cek = os.urandom(24)

        encoder = Encoder()
        jwe = encoder.encrypt_token(VALID_SIGNED_JWT.encode(), cek=cek)

        decoder = JWTDecryptor()
        with self.assertRaises(InvalidTokenException) as ite:
            decoder.decrypt_jwt_token(jwe.decode())
        self.assertIn("CEK incorrect length", ite.exception.value)

    def test_iv_not_96_bits(self):
        iv = os.urandom(45)

        encoder = Encoder()
        jwe = encoder.encrypt_token(VALID_SIGNED_JWT.encode(), iv=iv)

        decoder = JWTDecryptor()
        with self.assertRaises(InvalidTokenException) as ite:
            decoder.decrypt_jwt_token(jwe.decode())
            self.assertIn("IV incorrect length", ite.exception.value)

    def test_authentication_tag_not_128_bits(self):
        encoder = Encoder()
        jwe = encoder.encrypt_token(VALID_SIGNED_JWT.encode(), tag=os.urandom(10))

        decoder = JWTDecryptor()
        with self.assertRaises(InvalidTokenException) as ite:
            decoder.decrypt_jwt_token(jwe.decode())
        self.assertIn("'Authentication tag must be 16 bytes or longer", ite.exception.value)

    def test_authentication_tag_corrupted(self):
        encoder = Encoder()
        jwe = encoder.encrypt_token(VALID_SIGNED_JWT.encode(), tag=b'adssadsadsadsadasdasdasads')

        decoder = JWTDecryptor()
        with self.assertRaises(InvalidTokenException):
            decoder.decrypt_jwt_token(jwe.decode())

    def test_cipher_text_corrupted(self):
        encoder = Encoder()
        jwe = encoder.encrypt_token(VALID_SIGNED_JWT.encode())

        tokens = jwe.decode().split('.')
        jwe_protected_header = tokens[0]
        encrypted_key = tokens[1]
        encoded_iv = tokens[2]
        encoded_cipher_text = tokens[3]
        encoded_tag = tokens[4]

        corrupted_cipher = encoded_cipher_text[0:len(encoded_cipher_text) - 1]
        reassembled = jwe_protected_header + "." + encrypted_key + "." + encoded_iv + "." + corrupted_cipher + "." + encoded_tag

        decoder = JWTDecryptor()
        with self.assertRaises(InvalidTokenException):
            decoder.decrypt_jwt_token(reassembled)

if __name__ == '__main__':
    unittest.main()
