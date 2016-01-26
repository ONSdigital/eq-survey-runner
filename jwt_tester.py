from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.asymmetric import padding as asymmetic_padding

import jwt
import os
import base64

backend = default_backend()


class Encoder (object):
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
      cipher = Cipher(algorithms.AES(self.cek), modes.GCM(self.iv), backend=backend)
      encryptor = cipher.encryptor()

      encryptor.authenticate_additional_data(self._get_additional_authenticated_data())

      ciphertext = encryptor.update(text) + encryptor.finalize()
      tag = encryptor.tag

      encoded_ciphertext =  self._base_64_encode(ciphertext)
      encoded_tag = self._base_64_encode(tag)

      # assemble result
      jwe = self._jwe_protected_header() + "." + self._encrypted_key() + "." + self._encode_iv() + "." + encoded_ciphertext + "." + encoded_tag

      return jwe

  def _jwe_protected_header(self):
        return  self._base_64_encode(unicode('{"alg":"RSA-OAEP","enc":"A256GCM"}', "utf-8"))

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
        return self._base_64_encode(ciphertext)

  def _encode_iv(self):
        return self._base_64_encode(self.iv)

  def _get_additional_authenticated_data(self):
        return str(self._jwe_protected_header())

  def _base_64_encode(self, text):
        # strip the trailing = as they are padding to make the result a multiple of 4
        # the RFC does the same, as do other base64 libraries so this is a safe operation
        return base64.urlsafe_b64encode(text).strip("=")


class Decoder (object):
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
        print("Encoded tag " + encoded_tag)
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
        # if the text is not a multiple of 4 pad with trailing =
        # some base64 libraries don't pad data but Python is strict
        # and will throw a incorrect padding error if we don't do this
        if len(text) % 4 != 0:
            while len(text) % 4 != 0:
                text += "="
        return base64.urlsafe_b64decode(text)

    def _decrypt_ciphertext(self, cipher_text, iv, key, tag, jwe_protected_header):
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=backend)
        decryptor = cipher.decryptor()
        decryptor.authenticate_additional_data(jwe_protected_header)
        decrypted_token = decryptor.update(cipher_text) + decryptor.finalize()
        return decrypted_token

    def decode(self, token):
        token = jwt.decode(token, self.rrm_publickey)
        return token


if __name__ == '__main__':

    encoder = Encoder()
    print("Encoded JWE Header " + encoder._jwe_protected_header())

    payload = {'user': 'jimmy'}
    encoded_token = encoder.encode(payload)
    print("Encoded Token: " + encoded_token + "\n")

    encrypted_token = encoder.encrypt(encoded_token)
    print("Encrypted Token: " + encrypted_token + "\n")

    decoder = Decoder()
    decrypted_token = decoder.decrypt(encrypted_token)
    print("Decrypted Token: " + decrypted_token + "\n")

    decoded_token = decoder.decode(decrypted_token)
    print("Decoded token: ", decoded_token)

    with open("jimmy.jwt", "r") as token_file:
        encrypted_by_java = token_file.read().replace("\n", "")

    print("Token file " + encrypted_by_java + "\n")

    decoder = Decoder()
    decrypted_java_token = decoder.decrypt(encrypted_by_java)
    print ("Decrypted Token: " + decrypted_java_token + "\n")

    decoded_java_token = decoder.decode(decrypted_java_token)
    print ("Decoded token: ", decoded_java_token)
