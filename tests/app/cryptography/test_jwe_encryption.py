from app.cryptography.jwe_decryption import JWEDirDecrypter
from app.cryptography.jwe_encryption import JWEDirEncrypter
import os
import unittest


class TestJWEDecryption(unittest.TestCase):

    def test_decryption(self):
        cek = os.urandom(32)
        iv = os.urandom(12)

        plain_text = "test encryption"
        encrypter = JWEDirEncrypter(cek)

        encrypted_text = encrypter.encrypt(plain_text, iv)
        self.assertNotEqual(plain_text, encrypted_text)


if __name__ == '__main__':
    unittest.main()
