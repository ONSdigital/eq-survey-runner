from app.cryptography.jwe_encryption import JWEDirEncrypter
import os
import unittest


class TestJWEEncryption(unittest.TestCase):

    def test_decryption(self):
        cek = os.urandom(32)

        plain_text = "test encryption"
        encrypter = JWEDirEncrypter()

        encrypted_text = encrypter.encrypt(plain_text, cek)
        self.assertNotEqual(plain_text, encrypted_text, cek)


if __name__ == '__main__':
    unittest.main()
