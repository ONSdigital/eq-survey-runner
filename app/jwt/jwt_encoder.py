from cryptography.hazmat.backends.openssl.backend import backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from app import settings
from app.submitter.encrypter import Encrypter
import jwt
import os


class Encoder (Encrypter):
    def __init__(self):
        private_key = self._to_bytes(settings.EQ_RRM_PRIVATE_KEY)
        public_key = self._to_bytes(settings.EQ_SR_PUBLIC_KEY)
        self.private_key = serialization.load_pem_private_key(private_key, password=b'digitaleq', backend=backend)
        self.public_key = serialization.load_pem_public_key(public_key, backend=backend)

        # first generate a random key
        self.cek = os.urandom(32)  # 256 bit random CEK

        # now generate a random IV
        self.iv = os.urandom(12)  # 96 bit random IV

    def encode(self, payload):
        return jwt.encode(payload, self.private_key, algorithm="RS256", headers={'kid': 'EDCRRM', 'typ': 'jwt'})

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

        encoded_ciphertext = self._base_64_encode(ciphertext)
        encoded_tag = self._base_64_encode(tag)

        # assemble result
        jwe = jwe_protected_header + b"." + encrypted_key + b"." + self._encode_iv(iv) + b"." + encoded_ciphertext + b"." + encoded_tag

        return jwe
