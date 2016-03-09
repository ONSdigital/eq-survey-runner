from tests.app.authentication.encoder import Encoder
import os
import time


def generate_token():
    encoder = Encoder()
    user = os.getenv('USER', 'UNKNOWN')
    iat = time.time()
    exp = time.time() + (5 * 60)
    payload = {'user': user, 'iat': str(int(iat)), 'exp': str(int(exp))}
    token = encoder.encode(payload)
    encrypted_token = encoder.encrypt(token)
    return encrypted_token


if __name__ == '__main__':
    print("http://localhost:5000/session?token=" + generate_token().decode())
