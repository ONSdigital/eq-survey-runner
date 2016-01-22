from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import jwt


class Encoder:
  def __init__(self):
    with open("private.pem", "r") as key_file:
      self.key = serialization.load_pem_private_key(
        key_file.read(),
        password='digitaleq',
        backend=default_backend(),
      )

  def encode(self, payload):
    return jwt.encode(payload, self.key, algorithm="RS256")

if __name__ == '__main__':
    encoder = Encoder()

    payload = {'user': 'jimmy'}
    encoded_token = encoder.encode(payload)
    print (encoded_token)

