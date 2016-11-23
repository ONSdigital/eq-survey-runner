import base64

from app.utilities import strings

from cryptography.hazmat.backends.openssl.backend import backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers import modes


class JWEDecryptor(object):

    @staticmethod
    def _decrypt_cipher_text(cipher_text, iv, key, tag, jwe_protected_header):
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


class JWERSAOAEPDecryptor(JWEDecryptor):

    def __init__(self, private_key, password):

        self.private_key = serialization.load_pem_private_key(
            private_key.encode(),
            password=password.encode(),
            backend=backend,
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
        return signed_token

    def _decrypt_key(self, encrypted_key):
        decoded_key = self._base64_decode(encrypted_key)
        key = self.private_key.decrypt(decoded_key, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA1()), algorithm=hashes.SHA1(), label=None))
        return key


class JWEDirDecrypter(JWEDecryptor):

    def decrypt(self, token, cek):
        tokens = token.split('.')
        if len(tokens) != 5:
            raise ValueError("Incorrect size")
        jwe_protected_header = tokens[0]
        # encrypted_key is not used, would be tokens[1]
        encoded_iv = tokens[2]
        encoded_cipher_text = tokens[3]
        encoded_tag = tokens[4]

        iv = self._base64_decode(encoded_iv)
        tag = self._base64_decode(encoded_tag)
        cipher_text = self._base64_decode(encoded_cipher_text)

        decrypted_text = self._decrypt_cipher_text(cipher_text, iv, cek, tag, jwe_protected_header)
        decoded_text = self._base64_decode(strings.to_str(decrypted_text))
        return strings.to_str(decoded_text)
