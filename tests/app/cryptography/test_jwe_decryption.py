import os
import unittest

from app.cryptography.jwe_decryption import JWEDirDecrypter
from app.cryptography.jwe_encryption import JWEDirEncrypter


class TestJWEDecryption(unittest.TestCase):

    def test_decryption(self):
        cek = os.urandom(32)

        plain_text = "test decryption"
        encrypter = JWEDirEncrypter()
        decrypter = JWEDirDecrypter()

        encrypted_text = encrypter.encrypt(plain_text, cek)
        self.assertEqual(plain_text, decrypter.decrypt(encrypted_text, cek))


if __name__ == '__main__':
    unittest.main()
