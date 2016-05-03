from cryptography.hazmat.backends.openssl.backend import backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64


class JWEDirDecrypter(object):
    def __init__(self, cek):
        self.cek = cek

    def decrypt(self, token):
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

        decrypted_text = self._decrypt_cipher_text(cipher_text, iv, self.cek, tag, jwe_protected_header)
        return decrypted_text

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
