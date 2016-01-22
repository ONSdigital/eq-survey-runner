from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import jwt
import os
import base64

backend = default_backend()
key = 'sharedsecret1999'
iv = os.urandom(16)


class Encoder:
  def __init__(self):
    with open("private.pem", "r") as key_file:
      self.privatekey = serialization.load_pem_private_key(
        key_file.read(),
        password='digitaleq',
        backend=backend
      )
    with open("public.pem", "r") as key_file:
      self.publickey = serialization.load_pem_public_key(
        key_file.read(),
        backend=default_backend()
      )

  def encode(self, payload):
    return jwt.encode(payload, self.privatekey, algorithm="RS256")

  def decode(self, token):
      token = jwt.decode(token, self.publickey)
      return token

  def encrypt(self, token):
      padder = padding.PKCS7(128).padder()
      padded_data = padder.update(token) + padder.finalize()

      cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
      encryptor = cipher.encryptor()

      encrypted_text = encryptor.update(padded_data) + encryptor.finalize()

      return base64.b64encode(iv + encrypted_text)

  def decrypt(self, encrypted_token):
      data = base64.b64decode(encrypted_token)
      encryption_iv = data[:16]

      cipher = Cipher(algorithms.AES(key), modes.CBC(encryption_iv), backend=backend)
      decryptor = cipher.decryptor()
      decrypted_token = decryptor.update(data[16:])

      unpadder = padding.PKCS7(128).unpadder()
      unpadded_data = unpadder.update(decrypted_token) + unpadder.finalize()

      return unpadded_data


if __name__ == '__main__':
    encoder = Encoder()

    payload = {'user': 'jimmy'}
    encoded_token = encoder.encode(payload)
    print ("Encoded Token: " + encoded_token)
    encrypted_token = encoder.encrypt(encoded_token)
    #print ("Encrypted Token: " + encrypted_token)

    decrypted_token = encoder.decrypt(encrypted_token)

    print ("Decrypted Token: " + decrypted_token)

    decoded_token = encoder.decode(decrypted_token)

    print ("Decoded token: " , decoded_token)

