from cryptography.hazmat.backends.openssl.backend import backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from app.utilities import strings

import base64


class JWEDirEncrypter(object):
    def __init__(self, cek):
        self.cek = cek

    def _jwe_protected_header(self):
        return self._base_64_encode(b'{"alg":"dir","enc":"A256GCM"}')

    def _base_64_encode(self, text):
        # strip the trailing = as they are padding to make the result a multiple of 4
        # the RFC does the same, as do other base64 libraries so this is a safe operation
        return base64.urlsafe_b64encode(text).decode().strip("=").encode()

    def encrypt(self, json, iv):
        payload = self._base_64_encode(strings.to_bytes(json))
        jwe_protected_header = self._jwe_protected_header()

        cipher = Cipher(algorithms.AES(self.cek), modes.GCM(iv), backend=backend)
        encryptor = cipher.encryptor()

        encryptor.authenticate_additional_data(jwe_protected_header)

        ciphertext = encryptor.update(payload) + encryptor.finalize()

        tag = encryptor.tag

        encoded_ciphertext = self._base_64_encode(ciphertext)
        encoded_tag = self._base_64_encode(tag)

        # assemble result
        jwe = jwe_protected_header + b".." + self._base_64_encode(iv) + b"." + encoded_ciphertext + b"." + encoded_tag

        return strings.to_str(jwe)
