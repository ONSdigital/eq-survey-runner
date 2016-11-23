import json
import logging

from app import settings
from app.authentication.invalid_token_exception import InvalidTokenException
from app.authentication.no_token_exception import NoTokenException
from app.cryptography.jwe_decryption import JWERSAOAEPDecryptor
from app.utilities import strings

from cryptography.exceptions import InternalError
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.backends.openssl.backend import backend
from cryptography.hazmat.primitives import serialization

import jwt

IV_EXPECTED_LENGTH = 12
CEK_EXPECT_LENGTH = 32


class JWTDecryptor(JWERSAOAEPDecryptor):
    """
    JWT signed with JWS RS256 And encrypted with JWE RSA-OAEP
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        if settings.EQ_USER_AUTHENTICATION_RRM_PUBLIC_KEY is None or settings.EQ_USER_AUTHENTICATION_SR_PRIVATE_KEY is None \
                or settings.EQ_USER_AUTHENTICATION_SR_PRIVATE_KEY_PASSWORD is None:
            self.logger.fatal('KEYMAT not configured correctly.')
            raise OSError('KEYMAT not configured correctly.')
        else:
            super().__init__(settings.EQ_USER_AUTHENTICATION_SR_PRIVATE_KEY, settings.EQ_USER_AUTHENTICATION_SR_PRIVATE_KEY_PASSWORD)
            # oddly the python cryptography library needs these as bytes string
            rrm_public_key_as_bytes = strings.to_bytes(settings.EQ_USER_AUTHENTICATION_RRM_PUBLIC_KEY)
            self.rrm_public_key = serialization.load_pem_public_key(
                rrm_public_key_as_bytes,
                backend=backend,
            )

    def decode_signed_jwt_token(self, signed_token):
        try:
            if signed_token:
                logging.debug("Decoding signed JWT " + strings.to_str(signed_token))
                self._check_token(signed_token)
                token = jwt.decode(signed_token, self.rrm_public_key, algorithms=['RS256'],
                                   leeway=settings.EQ_JWT_LEEWAY_IN_SECONDS)
                if not token:
                    raise InvalidTokenException("Missing Payload")
                return token
            else:
                raise NoTokenException("JWT Missing")
        except (jwt.DecodeError,
                jwt.exceptions.InvalidAlgorithmError,
                jwt.exceptions.ExpiredSignatureError,
                jwt.exceptions.InvalidIssuedAtError) as e:
            raise InvalidTokenException(repr(e))

    def _check_token(self, token):
        token_as_str = strings.to_str(token)
        if token_as_str.count(".") != 2:
            raise InvalidTokenException("Invalid Token")

        # header_data, payload_data, signature_data
        header_data, payload_data, _ = token_as_str.split('.', maxsplit=2)

        self._check_headers(header_data)
        self._check_header_values(token_as_str)
        self._check_payload(payload_data)

    @staticmethod
    def _check_header_values(token):
        header = jwt.get_unverified_header(token)

        if not header:
            raise InvalidTokenException("Missing Headers")
        if not header.get('typ'):
            raise InvalidTokenException("Missing Type")
        if not header.get('alg'):
            raise InvalidTokenException("Missing Algorithm")
        if not header.get('kid'):
            raise InvalidTokenException("Missing kid")
        if header.get('typ').upper() != 'JWT':
            raise InvalidTokenException("Invalid Type")
        if header.get('alg').upper() != 'RS256':
            raise InvalidTokenException("Invalid Algorithm")
        if header.get('kid').upper() != 'EDCRRM':
            raise InvalidTokenException("Invalid Key Identifier")

    def _check_headers(self, header_data):
        try:
            headers = self._base64_decode(header_data)
            if not headers:
                raise InvalidTokenException("Missing Headers")
            self._check_for_duplicates(headers)
        except UnicodeDecodeError:
            raise InvalidTokenException("Corrupted Header")
        except ValueError as e:
            raise InvalidTokenException(repr(e))

    def _check_for_duplicates(self, headers):
        headers_as_str = strings.to_str(headers)
        json.loads(headers_as_str, object_pairs_hook=self._raise_exception_on_duplicates)

    @staticmethod
    def _raise_exception_on_duplicates(ordered_pairs):
        store = {}
        for key, value in ordered_pairs:
            if key in store:
                raise InvalidTokenException("Multiple " + key + " Headers")
            else:
                store[key] = value
        return store

    def _check_payload(self, payload_data):
        try:
            payload = self._base64_decode(payload_data)
            if not payload:
                raise InvalidTokenException("Missing Payload")
            payload_decoded = payload.decode()
            if payload_decoded == "{}":
                raise InvalidTokenException("Missing Payload")
            if payload_decoded.count("iat") == 0:
                raise InvalidTokenException("Missing iat claim")
            if payload_decoded.count("exp") == 0:
                raise InvalidTokenException("Missing exp claim")
            if payload_decoded.count("iat") > 1:
                raise InvalidTokenException("Multiple iat claims")
            if payload_decoded.count("exp") > 1:
                raise InvalidTokenException("Multiple exp claims")
        except (UnicodeDecodeError, IndexError):
            raise InvalidTokenException("Corrupted Payload")
        except ValueError as e:
            raise InvalidTokenException(repr(e))

    def decrypt_jwt_token(self, token):
        try:
            if token:
                logging.debug("Decrypting signed JWT " + strings.to_str(token))
                tokens = token.split('.')
                if len(tokens) != 5:
                    raise InvalidTokenException("Incorrect size")
                jwe_protected_header = tokens[0]
                self.__check_jwe_protected_header(jwe_protected_header)
                encrypted_key = tokens[1]
                encoded_iv = tokens[2]

                decrypted_key = self._decrypt_key(encrypted_key)
                iv = self._base64_decode(encoded_iv)
                if not self._check_iv_length(iv):
                    raise InvalidTokenException("IV incorrect length")
                if not self._check_cek_length(decrypted_key):
                    raise InvalidTokenException("CEK incorrect length")

                signed_token = super().decrypt(token)
                return self.decode_signed_jwt_token(signed_token)
            else:
                raise NoTokenException("JWT Missing")
        except (jwt.DecodeError, InvalidTag, InternalError, ValueError, AssertionError) as e:
            raise InvalidTokenException(repr(e))

    def __check_jwe_protected_header(self, header):
        header = self._base64_decode(header).decode()
        header_data = json.loads(header)
        if not header_data.get("alg"):
            raise InvalidTokenException("Missing Algorithm")
        if header_data.get("alg") != "RSA-OAEP":
            raise InvalidTokenException("Invalid Algorithm")
        if not header_data.get("enc"):
            raise InvalidTokenException("Missing Encoding")
        if header_data.get("enc") != "A256GCM":
            raise InvalidTokenException("Invalid Encoding")

    @staticmethod
    def _check_iv_length(iv):
        return len(iv) == IV_EXPECTED_LENGTH

    @staticmethod
    def _check_cek_length(cek):
        return len(cek) == CEK_EXPECT_LENGTH
