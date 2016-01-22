from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import jwt


class NoTokenException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class InvalidTokenException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class Decoder:

    def __init__(self):
      with open("public.pem", "r") as key_file:
        self.key = serialization.load_pem_public_key(
          key_file.read(),
          backend=default_backend()
        )

    def decode_token(self, encrypted_token):
      try:
          if encrypted_token:
              print self.key
              decrypted_token = jwt.decode(encrypted_token, self.key)
              print (decrypted_token)
              return decrypted_token
          else:
              raise NoTokenException("JWT Missing")
      except jwt.DecodeError as e:
          raise InvalidTokenException(repr(e))
