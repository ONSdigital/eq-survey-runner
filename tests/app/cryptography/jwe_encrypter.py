import base64
import os

from cryptography.hazmat.backends.openssl.backend import backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers import modes
from cryptography.hazmat.primitives.asymmetric import padding

from app.utilities import strings

KID = '709eb42cfee5570058ce0711f730bfbb7d4c8ade'


class Encoder(object):

    # password and key variables are dynamically assigned
    def __init__(self, private_key, public_key):

        if not len(private_key):
            raise ValueError('Invalid private key')

        self._public_key = public_key

        self._load_private_keys(private_key)

        # first generate a random key
        self.cek = os.urandom(32)  # 256 bit random CEK

        # now generate a random IV
        self.iv = os.urandom(12)  # 96 bit random IV

    def _load_private_keys(self, private_key):
        private_key_bytes = strings.to_bytes(private_key)

        self.private_key = serialization.load_pem_private_key(data=private_key_bytes,
                                                              password=None,
                                                              backend=backend)

    @staticmethod
    def _load_public_key(public_key):
        public_key_bytes = strings.to_bytes(public_key)
        return serialization.load_pem_public_key(data=public_key_bytes, backend=backend)

    def _jwe_protected_header(self, kid):
        return self._base_64_encode(bytes('{"alg":"RSA-OAEP","enc":"A256GCM","kid":"' + kid + '"}', 'utf-8'))

    def _encrypted_key(self, cek):

        public_key = self._load_public_key(self._public_key)

        ciphertext = public_key.encrypt(cek,
                                        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA1()), algorithm=hashes.SHA1(),
                                                     label=None))
        return self._base_64_encode(ciphertext)

    @staticmethod
    def _base_64_encode(text):
        # strip the trailing = as they are padding to make the result a multiple of 4
        # the RFC does the same, as do other base64 libraries so this is a safe operation
        return base64.urlsafe_b64encode(text).decode().strip("=").encode()

    def encrypt_token(self, text, kid, jwe_protected_header=None, encrypted_key=None, tag=None):
        """
        Overloading this method for test purposes, this allows us to modify the encrypted contents to test
        the decoder.
        :param kid:
        :param text: the text to encrypt
        :param jwe_protected_header: the protected header, providing this overrides the internal one
        :param encrypted_key: the encrypted cek, providing this overrides the encrypted internal one
        :param tag: the authentication tag, providing this overrides the generated one
        :return: an encoded and encrypted text
        """
        if jwe_protected_header is None:
            jwe_protected_header = self._jwe_protected_header(kid)
        else:
            jwe_protected_header = self._base_64_encode(jwe_protected_header)
        if encrypted_key is None:
            encrypted_key = self._encrypted_key(self.cek)

        cipher = Cipher(algorithms.AES(self.cek), modes.GCM(self.iv), backend=backend)
        encryptor = cipher.encryptor()

        encryptor.authenticate_additional_data(jwe_protected_header)

        ciphertext = encryptor.update(text) + encryptor.finalize()
        if tag is None:
            tag = encryptor.tag

        encoded_ciphertext = self._base_64_encode(ciphertext)
        encoded_tag = self._base_64_encode(tag)
        encoded_iv = self._base_64_encode(self.iv)

        # assemble result
        jwe = jwe_protected_header + b"." + encrypted_key + b"." + encoded_iv + b"." + encoded_ciphertext + b"." + encoded_tag

        return jwe
