import os

from app import settings
from app.cryptography.jwe_encryption import JWEEncrypter
from app.utilities import strings

from cryptography.hazmat.backends.openssl.backend import backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers import modes

import jwt

KID = 'EDCSR'


class Encrypter(JWEEncrypter):

    def __init__(self,
                 private_key=settings.EQ_SUBMISSION_SR_PRIVATE_SIGNING_KEY,
                 private_key_password=settings.EQ_SUBMISSION_SR_PRIVATE_SIGNING_KEY_PASSWORD,
                 public_key=settings.EQ_SUBMISSION_SDX_PUBLIC_KEY):

        self._load_keys(private_key, private_key_password, public_key)

        # first generate a random key
        self.cek = os.urandom(32)  # 256 bit random CEK

        # now generate a random IV
        self.iv = os.urandom(12)  # 96 bit random IV

    def _load_keys(self, private_key, private_key_password, public_key):
        private_key_bytes = strings.to_bytes(private_key)
        private_key_password_bytes = strings.to_bytes(private_key_password)
        public_key_bytes = strings.to_bytes(public_key)

        self.private_key = serialization.load_pem_private_key(data=private_key_bytes,
                                                              password=private_key_password_bytes,
                                                              backend=backend)
        self.public_key = serialization.load_pem_public_key(data=public_key_bytes, backend=backend)

    def _jwe_protected_header(self):
        return self._base_64_encode(b'{"alg":"RSA-OAEP","enc":"A256GCM"}')

    def _encrypted_key(self, cek):
        ciphertext = self.public_key.encrypt(cek, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA1()), algorithm=hashes.SHA1(), label=None))
        return self._base_64_encode(ciphertext)

    def _encode_iv(self, iv):
        return self._base_64_encode(iv)

    def _encode_and_signed(self, payload):
        return jwt.encode(payload, self.private_key, algorithm="RS256", headers={'kid': KID, 'typ': 'jwt'})

    def encrypt(self, json):
        payload = self._encode_and_signed(json)
        jwe_protected_header = self._jwe_protected_header()
        encrypted_key = self._encrypted_key(self.cek)

        cipher = Cipher(algorithms.AES(self.cek), modes.GCM(self.iv), backend=backend)
        encryptor = cipher.encryptor()

        encryptor.authenticate_additional_data(jwe_protected_header)

        ciphertext = encryptor.update(payload) + encryptor.finalize()

        tag = encryptor.tag

        encoded_ciphertext = self._base_64_encode(ciphertext)
        encoded_tag = self._base_64_encode(tag)

        # assemble result
        jwe = jwe_protected_header + b"." + encrypted_key + b"." + self._encode_iv(self.iv) + b"." + encoded_ciphertext + b"." + encoded_tag

        return strings.to_str(jwe)
