from cryptography.hazmat.backends.openssl.backend import backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from tests.app.authentication import TEST_DO_NOT_USE_SR_PUBLIC_PEM, TEST_DO_NOT_USE_RRM_PRIVATE_PEM

import jwt
import os
import base64


class Encoder (object):
    def __init__(self):
        private_key = self.__to_bytes(TEST_DO_NOT_USE_RRM_PRIVATE_PEM)
        public_key = self.__to_bytes(TEST_DO_NOT_USE_SR_PUBLIC_PEM)
        self.rrm_privatekey = serialization.load_pem_private_key(private_key, password=b'digitaleq', backend=backend)
        self.sr_publickey = serialization.load_pem_public_key(public_key, backend=backend)

        # first generate a random key
        self.cek = os.urandom(32)  # 256 bit random CEK

        # now generate a random IV
        self.iv = os.urandom(12)  # 96 bit random IV

    def __to_bytes(self, bytes_or_str):
        if isinstance(bytes_or_str, str):
            value = bytes_or_str.encode()
        else:
            value = bytes_or_str
        return value

    def encode(self, payload):
        return jwt.encode(payload, self.rrm_privatekey, algorithm="RS256", headers={'kid': 'EDCRRM', 'typ': 'jwt'})

    def encrypt(self, text, jwe_protected_header=None, cek=None, iv=None, encrypted_key=None, tag=None):
        if jwe_protected_header is None:
            jwe_protected_header = self._jwe_protected_header()
        if cek is None:
            cek = self.cek
        if iv is None:
            iv = self.iv
        if encrypted_key is None:
            encrypted_key = self._encrypted_key(cek)

        cipher = Cipher(algorithms.AES(cek), modes.GCM(iv), backend=backend)
        encryptor = cipher.encryptor()

        encryptor.authenticate_additional_data(self._jwe_protected_header())

        ciphertext = encryptor.update(text) + encryptor.finalize()
        if tag is None:
            tag = encryptor.tag

        encoded_ciphertext = self.base_64_encode(ciphertext)
        encoded_tag = self.base_64_encode(tag)

        # assemble result
        jwe = jwe_protected_header + b"." + encrypted_key + b"." + self._encode_iv(iv) + b"." + encoded_ciphertext + b"." + encoded_tag

        return jwe

    def _jwe_protected_header(self):
        return self.base_64_encode(b'{"alg":"RSA-OAEP","enc":"A256GCM"}')

    def _encrypted_key(self, cek):
        ciphertext = self.sr_publickey.encrypt(cek, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA1()), algorithm=hashes.SHA1(), label=None))
        return self.base_64_encode(ciphertext)

    def _encode_iv(self, iv):
        return self.base_64_encode(iv)

    def base_64_encode(self, text):
        # strip the trailing = as they are padding to make the result a multiple of 4
        # the RFC does the same, as do other base64 libraries so this is a safe operation
        return base64.urlsafe_b64encode(text).decode().strip("=").encode()
