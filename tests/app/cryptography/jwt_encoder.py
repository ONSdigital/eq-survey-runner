import jwt
from cryptography.hazmat.backends.openssl.backend import backend
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers import modes

from app.submitter.encrypter import Encrypter

KID = 'EDCRRM'


class Encoder(Encrypter):
    def encode(self, payload):
        return jwt.encode(payload, self.private_key, algorithm="RS256", headers={'kid': KID, 'typ': 'jwt'})

    def encrypt_token(self, text, jwe_protected_header=None, encrypted_key=None, tag=None):
        """
        Overloading this method for test purposes, this allows us to modify the encrypted contents to test
        the decoder.
        :param text: the text to encrypt
        :param jwe_protected_header: the protected header, providing this overrides the internal one
        :param encrypted_key: the encrypted cek, providing this overrides the encrypted internal one
        :param tag: the authentication tag, providing this overrides the generated one
        :return: an encoded and encrypted text
        """
        if jwe_protected_header is None:
            jwe_protected_header = self._jwe_protected_header()
        if encrypted_key is None:
            encrypted_key = self._encrypted_key(self.cek)

        cipher = Cipher(algorithms.AES(self.cek), modes.GCM(self.iv), backend=backend)
        encryptor = cipher.encryptor()

        encryptor.authenticate_additional_data(self._jwe_protected_header())

        ciphertext = encryptor.update(text) + encryptor.finalize()
        if tag is None:
            tag = encryptor.tag

        encoded_ciphertext = self._base_64_encode(ciphertext)
        encoded_tag = self._base_64_encode(tag)

        # assemble result
        jwe = jwe_protected_header + b"." + encrypted_key + b"." + self._encode_iv(self.iv) + b"." + encoded_ciphertext + b"." + encoded_tag

        return jwe
