from cryptography.hazmat.backends.openssl.backend import backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidTag, InternalError

from app.authentication.invalid_token_exception import InvalidTokenException
from app.authentication.no_token_exception import NoTokenException
import base64
import jwt
import logging


class Decoder (object):
    def __init__(self, rrm_public_key, sr_private_key, sr_private_key_password=None):
        # oddly the python cryptography library needs these as bytes string
        rrm_public_key_as_bytes = self.__to_bytes(rrm_public_key)
        sr_private_key_as_bytes = self.__to_bytes(sr_private_key)

        self.rrm_public_key = serialization.load_pem_public_key(
            rrm_public_key_as_bytes,
            backend=backend
        )
        self.sr_private_key = serialization.load_pem_private_key(
            sr_private_key_as_bytes,
            password=sr_private_key_password.encode(),
            backend=backend
        )

    def _check_token(self, token):
        iat = token.get('iat')
        if not iat:
            raise InvalidTokenException("Missing iat claim")
        exp = token.get('exp')
        if not exp:
            raise InvalidTokenException("Missing exp claim")

    def _check_payload(self, signed_token):
        token = self.__to_str(signed_token)
        try:
            payload_data = token.split('.', 2)[1]
            payload = self._base64_decode(payload_data)
            p = payload.decode()
            if p.count("iat") > 1:
                raise InvalidTokenException("Multiple iat claims")
            if p.count("exp") > 1:
                raise InvalidTokenException("Multiple exp claims")
        except (UnicodeDecodeError, IndexError):
            raise InvalidTokenException("Corrupted Payload")
        except ValueError as e:
            raise InvalidTokenException(repr(e))

    def decode_jwt_token(self, token):
        try:
            if token:
                logging.debug("Decoding JWT " + self.__to_str(token))
                self._check_payload(token)
                token = jwt.decode(token, verify=False)
                self._check_token(token)
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
                self._check_headers(signed_token)
                self._check_payload(signed_token)
                token = jwt.decode(signed_token, self.rrm_public_key, algorithms=['RS256'])
                self._check_token(token)
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

    def _check_headers(self, signed_token):
        token = self.__to_str(signed_token)
        header_data = token.split('.', 1)[0]
        try:
            headers = self._base64_decode(header_data)
            self.__check_for_duplicates(headers)
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

    def __check_for_duplicates(self, headers):
        h = self.__to_str(headers)
        if h.count("typ") > 1:
            raise InvalidTokenException("Multiple Type Headers")
        if h.count("alg") > 1:
            raise InvalidTokenException("Multiple Algorithm Headers")
        if h.count("kid") > 1:
            raise InvalidTokenException("Multiple KID headers")

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
        if header.count("alg") == 0:
            raise InvalidTokenException("Missing Algorithm")
        if header.count("RSA-OAEP") == 0:
            raise InvalidTokenException("Invalid Algorithm")
        if header.count("enc") == 0:
            raise InvalidTokenException("Missing Encoding")
        if header.count("A256GCM") == 0:
            raise InvalidTokenException("Invalid Encoding")

    def _check_iv_length(self, iv):
        return len(iv) == 12

    def _check_cek_length(self, cek):
        return len(cek) == 32

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
