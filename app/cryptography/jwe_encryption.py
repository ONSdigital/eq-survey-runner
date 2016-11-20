import base64
import json
import os

from app.utilities import strings

from cryptography.hazmat.backends.openssl.backend import backend
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers import modes


class JWEEncrypter(object):

    @staticmethod
    def _base_64_encode(text):
        # strip the trailing = as they are padding to make the result a multiple of 4
        # the RFC does the same, as do other base64 libraries so this is a safe operation
        return base64.urlsafe_b64encode(text).decode().strip("=").encode()


ALG_HEADER = "alg"
ALG = "dir"
ENC_HEADER = "enc"
ENC = "A256GCM"
KID_HEADER = "kid"
KID = "1,1"


class JWEDirEncrypter(JWEEncrypter):

    def _jwe_protected_header(self):

        protected_header = {ALG_HEADER: ALG, ENC_HEADER: ENC, KID_HEADER: KID}
        return self._base_64_encode(json.dumps(protected_header).encode())

    def encrypt(self, json_data, cek):
        # 96 bit random IV
        iv = os.urandom(12)
        payload = self._base_64_encode(strings.to_bytes(json_data))
        jwe_protected_header = self._jwe_protected_header()

        cipher = Cipher(algorithms.AES(cek), modes.GCM(iv), backend=backend)
        encryptor = cipher.encryptor()

        encryptor.authenticate_additional_data(jwe_protected_header)

        ciphertext = encryptor.update(payload) + encryptor.finalize()

        tag = encryptor.tag

        encoded_ciphertext = self._base_64_encode(ciphertext)
        encoded_tag = self._base_64_encode(tag)

        # assemble result
        jwe = jwe_protected_header + b".." + self._base_64_encode(iv) + b"." + encoded_ciphertext + b"." + encoded_tag

        return strings.to_str(jwe)
