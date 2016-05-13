from app.cryptography.jwe_decryption import JWEDirDecrypter
from app.cryptography.jwe_encryption import JWEDirEncrypter
import os
import unittest


class TestJWEDecryption(unittest.TestCase):

    def test_decryption(self):
        cek = os.urandom(32)

        plain_text = "test decryption"
        encrypter = JWEDirEncrypter(cek)
        decrypter = JWEDirDecrypter(cek)

        encrypted_text = encrypter.encrypt(plain_text)
        self.assertEqual(plain_text, decrypter.decrypt(encrypted_text))


if __name__ == '__main__':
    unittest.main()
