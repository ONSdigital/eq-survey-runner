from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from invalid_token_exception import InvalidTokenException
from no_token_exception import NoTokenException
import base64
import jwt


class Decoder:
  def __init__(self):
    self.backend = default_backend()
    self.secret = 'sharedsecret1999'

    with open("public.pem", "r") as key_file:
      self.key = serialization.load_pem_public_key(
        key_file.read(),
        backend=default_backend()
      )

  def decode_jwt_token(self, decrypted_token):
    try:
      if decrypted_token:
        token = jwt.decode(decrypted_token, self.key)
        print ("JWT Token ", token)
        return token
      else:
        raise NoTokenException("JWT Missing")
    except jwt.DecodeError as e:
        raise InvalidTokenException(repr(e))

  def decrypt_token(self, encrypted_token):
    data = base64.urlsafe_b64decode(str(encrypted_token))
    encryption_iv = data[:16]

    cipher = Cipher(algorithms.AES(self.secret), modes.CBC(encryption_iv), backend=self.backend)
    decryptor = cipher.decryptor()
    decrypted_token = decryptor.update(data[16:])

    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(decrypted_token) + unpadder.finalize()
    return self.decode_jwt_token(unpadded_data)
