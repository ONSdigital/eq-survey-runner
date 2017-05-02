import os
import unittest

from app.authentication.invalid_token_exception import InvalidTokenException
from app.authentication.jwt_decoder import JWTDecryptor
from app.cryptography.jwt_encoder import Encoder
from tests.app.authentication import (
    TEST_DO_NOT_USE_SR_PRIVATE_PEM,
    TEST_DO_NOT_USE_SR_PUBLIC_KEY,
    TEST_DO_NOT_USE_RRM_PRIVATE_KEY,
    TEST_DO_NOT_USE_RRM_PUBLIC_PEM,
    TEST_DO_NOT_USE_PASSWORD,
    VALID_JWE,
    VALID_SIGNED_JWT
)


class JWETest(unittest.TestCase):
    def setUp(self):
        self.decryptor_args = (
            TEST_DO_NOT_USE_SR_PRIVATE_PEM,
            TEST_DO_NOT_USE_PASSWORD,
            TEST_DO_NOT_USE_RRM_PUBLIC_PEM
        )

        self.encoder_args = (
            TEST_DO_NOT_USE_RRM_PRIVATE_KEY,
            TEST_DO_NOT_USE_PASSWORD,
            TEST_DO_NOT_USE_SR_PUBLIC_KEY
        )
        self.leeway = 120

    def test_valid_jwe(self):
        decoder = JWTDecryptor(*self.decryptor_args)
        token = decoder.decrypt_jwt_token(VALID_JWE, self.leeway)
        self.assertEqual("jimmy", token.get("user"))

    def test_does_not_contain_four_instances_of_full_stop(self):
        jwe = VALID_JWE.replace('.', '', 1)

        self.assertInDecryptException(jwe, "Incorrect size")

    def test_missing_algorithm(self):
        jwe_protected_header = b'{"enc":"A256GCM"}'
        encoder = Encoder(*self.encoder_args)
        jwe = encoder.encrypt_token(VALID_SIGNED_JWT.encode(), jwe_protected_header=encoder._base_64_encode(jwe_protected_header))  # pylint: disable=protected-access

        self.assertInDecryptException(jwe.decode(), "Missing Algorithm")

    def test_invalid_algorithm(self):
        jwe_protected_header = b'{"alg":"PBES2_HS256_A128KW","enc":"A256GCM"}'
        encoder = Encoder(*self.encoder_args)
        jwe = encoder.encrypt_token(VALID_SIGNED_JWT.encode(), jwe_protected_header=encoder._base_64_encode(jwe_protected_header))  # pylint: disable=protected-access

        self.assertInDecryptException(jwe.decode(), "Invalid Algorithm")

    def test_enc_missing(self):
        jwe_protected_header = b'{"alg":"RSA-OAEP"}'

        encoder = Encoder(*self.encoder_args)
        jwe = encoder.encrypt_token(VALID_SIGNED_JWT.encode(),
                                    jwe_protected_header=encoder._base_64_encode(jwe_protected_header))  # pylint: disable=protected-access

        self.assertInDecryptException(jwe.decode(), "Missing Encoding")

    def test_invalid_enc(self):
        jwe_protected_header = b'{"alg":"RSA-OAEP","enc":"A128GCM"}'
        encoder = Encoder(*self.encoder_args)
        jwe = encoder.encrypt_token(VALID_SIGNED_JWT.encode(),
                                    jwe_protected_header=encoder._base_64_encode(jwe_protected_header))  # pylint: disable=protected-access

        self.assertInDecryptException(jwe.decode(), "Invalid Encoding")

    def test_jwe_header_contains_alg_twice(self):
        jwe_protected_header = b'{"alg":"RSA-OAEP","alg":"RSA-OAEP","enc":"A256GCM"}'
        encoder = Encoder(*self.encoder_args)
        jwe = encoder.encrypt_token(VALID_SIGNED_JWT.encode(),
                                    jwe_protected_header=encoder._base_64_encode(jwe_protected_header))  # pylint: disable=protected-access

        self.assertInDecryptException(jwe.decode(), "InvalidTag")

    def test_jwe_header_only_contains_alg_and_enc(self):
        jwe_protected_header = b'{"alg":"RSA-OAEP","enc":"A256GCM", "test":"test"}'
        encoder = Encoder(*self.encoder_args)
        jwe = encoder.encrypt_token(VALID_SIGNED_JWT.encode(),
                                    jwe_protected_header=encoder._base_64_encode(jwe_protected_header))  # pylint: disable=protected-access

        self.assertInDecryptException(jwe.decode(), "InvalidTag")

    def test_jwe_key_not_2048_bits(self):
        cek = os.urandom(32)

        encoder = Encoder(*self.encoder_args)
        encoder.cek = cek
        encrypted_key = encoder._encrypted_key(cek)  # pylint: disable=protected-access
        encrypted_key = encrypted_key[0:len(encrypted_key) - 2]
        jwe = encoder.encrypt_token(VALID_SIGNED_JWT.encode(), encrypted_key=encrypted_key)

        self.assertInDecryptException(jwe.decode(), "ValueError")

    def test_cek_not_256_bits(self):
        cek = os.urandom(24)

        encoder = Encoder(*self.encoder_args)
        encoder.cek = cek
        jwe = encoder.encrypt_token(VALID_SIGNED_JWT.encode())

        self.assertInDecryptException(jwe.decode(), "CEK incorrect length")

    def test_iv_not_96_bits(self):
        iv = os.urandom(45)

        encoder = Encoder(*self.encoder_args)
        encoder.iv = iv
        jwe = encoder.encrypt_token(VALID_SIGNED_JWT.encode())

        self.assertInDecryptException(jwe.decode(), "IV incorrect length")

    def test_authentication_tag_not_128_bits(self):
        encoder = Encoder(*self.encoder_args)
        jwe = encoder.encrypt_token(VALID_SIGNED_JWT.encode(), tag=os.urandom(10))

        self.assertInDecryptException(jwe.decode(), "'Authentication tag must be 16 bytes or longer")

    def test_authentication_tag_corrupted(self):
        encoder = Encoder(*self.encoder_args)
        jwe = encoder.encrypt_token(VALID_SIGNED_JWT.encode(), tag=b'adssadsadsadsadasdasdasads')

        decoder = JWTDecryptor(*self.decryptor_args)
        with self.assertRaises(InvalidTokenException):
            decoder.decrypt_jwt_token(jwe.decode(), self.leeway)

    def test_cipher_text_corrupted(self):
        encoder = Encoder(*self.encoder_args)
        jwe = encoder.encrypt_token(VALID_SIGNED_JWT.encode())

        tokens = jwe.decode().split('.')
        jwe_protected_header = tokens[0]
        encrypted_key = tokens[1]
        encoded_iv = tokens[2]
        encoded_cipher_text = tokens[3]
        encoded_tag = tokens[4]

        corrupted_cipher = encoded_cipher_text[0:len(encoded_cipher_text) - 1]
        reassembled = jwe_protected_header + "." + encrypted_key + "." + encoded_iv + "." + corrupted_cipher + "." + encoded_tag

        decoder = JWTDecryptor(*self.decryptor_args)
        with self.assertRaises(InvalidTokenException):
            decoder.decrypt_jwt_token(reassembled, self.leeway)

    def assertInDecryptException(self, jwe, error):
        decoder = JWTDecryptor(*self.decryptor_args)
        with self.assertRaises(InvalidTokenException) as ite:
            decoder.decrypt_jwt_token(jwe, self.leeway)

        if error not in ite.exception.value:
            raise AssertionError('"{}" not found in decrypt exception'.format(error))

if __name__ == '__main__':
    unittest.main()
