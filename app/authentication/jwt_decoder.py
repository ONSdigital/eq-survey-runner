from cryptography.hazmat.backends.openssl.backend import backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidTag, InternalError

from app.authentication.invalid_token_exception import InvalidTokenException
from app.authentication.no_token_exception import NoTokenException
from app import settings
import base64
import jwt
import logging
import json

IV_EXPECTED_LENGTH = 12
CEK_EXPECT_LENGTH = 32


class Decoder (object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        if settings.EQ_RRM_PUBLIC_KEY is None or settings.EQ_SR_PRIVATE_KEY is None or settings.EQ_SR_PRIVATE_KEY_PASSWORD is None:
            self.logger.fatal('KEYMAT not configured correctly.')
            raise OSError('KEYMAT not configured correctly.')
        else:
            # oddly the python cryptography library needs these as bytes string
            rrm_public_key_as_bytes = self.__to_bytes(settings.EQ_RRM_PUBLIC_KEY)
            sr_private_key_as_bytes = self.__to_bytes(settings.EQ_SR_PRIVATE_KEY)

            self.rrm_public_key = serialization.load_pem_public_key(
                rrm_public_key_as_bytes,
                backend=backend
            )
            self.sr_private_key = serialization.load_pem_private_key(
                sr_private_key_as_bytes,
                password=settings.EQ_SR_PRIVATE_KEY_PASSWORD.encode(),
                backend=backend
            )

    def decode_jwt_token(self, token):
        try:
            if token:
                logging.debug("Decoding JWT " + self.__to_str(token))
                self._check_payload(self.__to_str(token))
                token = jwt.decode(token, verify=False)
                return token
            else:
                raise NoTokenException("JWT Missing")
        except jwt.DecodeError as e:
            raise InvalidTokenException(repr(e))
        except ValueError as e:
            raise InvalidTokenException(repr(e))

    def decode_signed_jwt_token(self, signed_token):
        try:
            if signed_token:
                logging.debug("Decoding signed JWT " + self.__to_str(signed_token))
                self._check_token(signed_token)
                token = jwt.decode(signed_token, self.rrm_public_key, algorithms=['RS256'])
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
        token_as_str = self.__to_str(token)
        if token_as_str.count(".") != 2:
            raise InvalidTokenException("Invalid Token")
        self._check_headers(token_as_str)
        self._check_payload(token_as_str)
        return

    def _check_headers(self, token):
        header_data, payload_data, signature_data = token.split('.', maxsplit=2)
        try:
            headers = self._base64_decode(header_data)
            if not headers:
                raise InvalidTokenException("Missing Headers")
            self._check_for_duplicates(headers)
        except UnicodeDecodeError:
            raise InvalidTokenException("Corrupted Header")
        except ValueError as e:
            raise InvalidTokenException(repr(e))

        header = jwt.get_unverified_header(token)
        if not header:
            raise InvalidTokenException("Missing Headers")
        if not header.get('typ'):
            raise InvalidTokenException("Missing Type")
        if not header.get('alg'):
            raise InvalidTokenException("Missing Algorithm")
        if not header.get('kid'):
            raise InvalidTokenException("Missing kid")
        if "JWT" != header.get('typ').upper():
            raise InvalidTokenException("Invalid Type")
        if "RS256" != header.get('alg').upper():
            raise InvalidTokenException("Invalid Algorithm")
        if "EDCRRM" != header.get('kid').upper():
            raise InvalidTokenException("Invalid Key Identifier")

    def _check_for_duplicates(self, headers):
        headers_as_str = self.__to_str(headers)
        json.loads(headers_as_str, object_pairs_hook=self._raise_exception_on_duplicates)

    def _raise_exception_on_duplicates(self, ordered_pairs):
        store = {}
        for key, value in ordered_pairs:
            if key in store:
                raise InvalidTokenException("Multiple " + key + " Headers")
            else:
                store[key] = value
        return store

    def _check_payload(self, token):
        try:
            header_data, payload_data, signature_data = token.split('.', maxsplit=2)
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

    def __to_str(self, bytes_or_str):
        if isinstance(bytes_or_str, bytes):
            value = bytes_or_str.decode()
        else:
            value = bytes_or_str
        return value

    def __to_bytes(self, bytes_or_str):
        if isinstance(bytes_or_str, str):
            value = bytes_or_str.encode()
        else:
            value = bytes_or_str
        return value

    def decrypt_jwt_token(self, token):
        try:
            if token:
                logging.debug("Decrypting signed JWT " + self.__to_str(token))
                tokens = token.split('.')
                if len(tokens) != 5:
                    raise InvalidTokenException("Incorrect size")
                jwe_protected_header = tokens[0]
                self.__check_jwe_protected_header(jwe_protected_header)
                encrypted_key = tokens[1]
                encoded_iv = tokens[2]
                encoded_cipher_text = tokens[3]
                encoded_tag = tokens[4]

                decrypted_key = self._decrypt_key(encrypted_key)
                iv = self._base64_decode(encoded_iv)
                if not self._check_iv_length(iv):
                    raise InvalidTokenException("IV incorrect length")
                if not self._check_cek_length(decrypted_key):
                    raise InvalidTokenException("CEK incorrect length")
                tag = self._base64_decode(encoded_tag)
                cipher_text = self._base64_decode(encoded_cipher_text)

                signed_token = self._decrypt_cipher_text(cipher_text, iv, decrypted_key, tag, jwe_protected_header)
                return self.decode_signed_jwt_token(signed_token)
            else:
                raise NoTokenException("JWT Missing")
        except (jwt.DecodeError, InvalidTag, InternalError, ValueError) as e:
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

    def _check_iv_length(self, iv):
        return len(iv) == IV_EXPECTED_LENGTH

    def _check_cek_length(self, cek):
        return len(cek) == CEK_EXPECT_LENGTH

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
