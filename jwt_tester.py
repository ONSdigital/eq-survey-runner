from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.asymmetric import padding as asymmetic_padding

import jwt
import os
import base64

backend = default_backend()

class Encoder:
  def __init__(self):
    with open("rrm-private.pem", "r") as key_file:
      self.rrm_privatekey = serialization.load_pem_private_key(
        key_file.read(),
        password='digitaleq',
        backend=backend
      )

    with open("sr-public.pem", "r") as key_file:
      self.sr_publickey = serialization.load_pem_public_key(
        key_file.read(),
        backend=default_backend()
      )
    # first generate a random key
    self.cek = os.urandom(32) # 256 bit random CEK
    # now generate a random IV
    self.iv = os.urandom(12) # 96 bit random IV

  def encode(self, payload):
    return jwt.encode(payload, self.rrm_privatekey, algorithm="RS256")

  def encrypt(self, text):
      padder = padding.PKCS7(128).padder()
      padded_data = padder.update(text) + padder.finalize()

      cipher = Cipher(algorithms.AES(self.cek), modes.GCM(self.iv), backend=backend)
      encryptor = cipher.encryptor()

      encryptor.authenticate_additional_data(self._get_additional_authenticated_data())

      ciphertext = encryptor.update(padded_data) + encryptor.finalize()
      tag = encryptor.tag

      encoded_ciphertext = base64.urlsafe_b64encode(ciphertext)
      encoded_tag = base64.urlsafe_b64encode(tag)

      # assemble result
      jwe = self._jwe_protected_header() + "." + self._encrypted_key() + "." + self._encode_iv() + "." + encoded_ciphertext + "." + encoded_tag

      return jwe

  def _jwe_protected_header(self):
        return base64.urlsafe_b64encode(unicode('{"alg":"RSA-OAEP","enc":"A256GCM"}', "utf-8"))

  def _encrypted_key(self):
        # initially encrypt using a shared secret, though this needs to be the survey runners public key eventually
        ciphertext = self.sr_publickey.encrypt(
          self.cek,
          asymmetic_padding.OAEP(
            mgf=asymmetic_padding.MGF1(algorithm=hashes.SHA1()),
            algorithm=hashes.SHA1(),
            label=None
          )
        )
        return base64.urlsafe_b64encode(ciphertext)

  def _encode_iv(self):
        return base64.urlsafe_b64encode(self.iv)

  def _get_additional_authenticated_data(self):
        return str(self._jwe_protected_header())


class Decoder:
    def __init__(self):
        with open("rrm-public.pem", "r") as key_file:
            self.rrm_publickey = serialization.load_pem_public_key(
              key_file.read(),
              backend=default_backend()
            )
        with open("sr-private.pem", "r") as key_file:
            self.sr_privatekey = serialization.load_pem_private_key(
              key_file.read(),
              password='digitaleq',
              backend=backend
            )

    def decrypt(self, token):
        tokens = token.split('.')
        if len(tokens) != 5:
          raise Exception
        jwe_protected_header = tokens[0]
        encrypted_key = tokens[1]
        encoded_iv = tokens[2]
        encoded_ciphertext = tokens[3]
        encoded_tag = tokens[4]

        decrypted_key = self._decrypt_key(encrypted_key)
        iv = self._base64_decode(encoded_iv)
        tag = self._base64_decode(encoded_tag)
        cipher_text = self._base64_decode(encoded_ciphertext)

        return self._decrypt_ciphertext(cipher_text, iv, decrypted_key, tag, jwe_protected_header)

    def _decrypt_key(self, encrypted_key):
        decoded_key = self._base64_decode(encrypted_key)
        key = self.sr_privatekey.decrypt(
                      decoded_key,
                      asymmetic_padding.OAEP(
                        mgf=asymmetic_padding.MGF1(algorithm=hashes.SHA1()),
                        algorithm=hashes.SHA1(),
                        label=None
                      )
                    )
        return key

    def _base64_decode(self, text):
        return base64.urlsafe_b64decode(text)

    def _decrypt_ciphertext(self, cipher_text, iv, key, tag, jwe_protected_header):
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=backend)
        decryptor = cipher.decryptor()
        decryptor.authenticate_additional_data(jwe_protected_header)
        decrypted_token = decryptor.update(cipher_text) + decryptor.finalize()

        unpadder = padding.PKCS7(128).unpadder()
        unpadded_data = unpadder.update(decrypted_token) + unpadder.finalize()

        return unpadded_data

    def decode(self, token):
        token = jwt.decode(token, self.rrm_publickey)
        return token


if __name__ == '__main__':

    encoder = Encoder()
    print ("Encoded JWE Header " + encoder._jwe_protected_header())

    payload = {'user': 'jimmy'}
    encoded_token = encoder.encode(payload)
    print ("Encoded Token: " + encoded_token + "\n")

    encrypted_token = encoder.encrypt(encoded_token)
    print ("Encrypted Token: " + encrypted_token + "\n")

    decoder = Decoder()
    decrypted_token = decoder.decrypt(encrypted_token)
    print ("Decrypted Token: " + decrypted_token + "\n")

    decoded_token = decoder.decode(decrypted_token)
    print ("Decoded token: ", decoded_token)

