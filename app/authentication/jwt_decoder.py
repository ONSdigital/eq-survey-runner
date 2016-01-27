from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from app.authentication.invalid_token_exception import InvalidTokenException
from app.authentication.no_token_exception import NoTokenException
import base64
import jwt


class Decoder (object):
    def __init__(self, rrm_public_key, sr_private_key, sr_private_key_password=None):
        self.rrm_public_key = serialization.load_pem_public_key(
                    rrm_public_key,
                    backend=default_backend()
        )
        self.sr_private_key = serialization.load_pem_private_key(
                    sr_private_key,
                    password=sr_private_key_password.encode(),
                    backend=default_backend()
        )

    def decode_jwt_token(self, token):
        try:
            if token:
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
                token = jwt.decode(signed_token, self.rrm_public_key)
                print("JWT Token ", token)
                return token
            else:
                raise NoTokenException("JWT Missing")
        except jwt.DecodeError as e:
            raise InvalidTokenException(repr(e))

    def decrypt_jwt_token(self, token):
        try:
            if token:
                tokens = token.split('.')
                if len(tokens) != 5:
                    raise InvalidTokenException("Incorrect size")
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
                return self.decode_signed_jwt_token(signed_token)
            else:
                raise NoTokenException("JWT Missing")
        except jwt.DecodeError as e:
            raise InvalidTokenException(repr(e))

    def _decrypt_key(self, encrypted_key):
        decoded_key = self._base64_decode(encrypted_key)
        key = self.sr_private_key.decrypt(decoded_key, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA1()), algorithm=hashes.SHA1(), label=None))
        return key

    def _decrypt_cipher_text(self, cipher_text, iv, key, tag, jwe_protected_header):
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
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

