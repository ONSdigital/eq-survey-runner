import unittest
import time
import logging
import os
from app import settings
from app import create_app
from tests.app.authentication.encoder import Encoder
from tests.app.authentication import TEST_DO_NOT_USE_RRM_PUBLIC_PEM, TEST_DO_NOT_USE_SR_PRIVATE_PEM


class FlaskClientAuthenticationTestCase(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)

        settings.EQ_RRM_PUBLIC_KEY = TEST_DO_NOT_USE_RRM_PUBLIC_PEM
        settings.EQ_SR_PRIVATE_KEY = TEST_DO_NOT_USE_SR_PRIVATE_PEM

        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        self.app_context.pop()

    def test_no_token(self):
        # set to production mode
        settings.EQ_PRODUCTION = 'True'
        response = self.client.get('/')
        self.assertEquals(401, response.status_code)

    def test_invalid_token(self):
        # set to production mode
        settings.EQ_PRODUCTION = 'True'
        token = "invalid"
        response = self.client.get('/?token=' + token)
        self.assertEquals(403, response.status_code)

    def test_fully_encrypted(self):
        # set to production mode
        settings.EQ_PRODUCTION = 'True'
        encoder = Encoder()
        iat = time.time()
        exp = time.time() + (5 * 60)
        payload = {'user': 'jimmy', 'iat': str(int(iat)), 'exp': str(int(exp))}
        token = encoder.encode(payload)
        encrypted_token = encoder.encrypt(token)
        response = self.client.get('/?token=' + encrypted_token.decode())
        self.assertEquals(200, response.status_code)

    def test_signed(self):
        # set to dev mode - production does not allow unencrypted
        settings.EQ_PRODUCTION = 'False'
        encoder = Encoder()
        iat = time.time()
        exp = time.time() + (5 * 60)
        payload = {'user': 'jimmy', 'iat': str(int(iat)), 'exp': str(int(exp))}
        token = encoder.encode(payload)
        response = self.client.get('/?token=' + token.decode())
        self.assertEquals(200, response.status_code)

    def test_encoded(self):
        # set to dev mode - production does not allow unencrypted and unsigned
        settings.EQ_PRODUCTION = 'False'
        encoder = Encoder()
        iat = time.time()
        exp = time.time() + (5 * 60)
        payload = {'user': 'jimmy', 'iat': str(int(iat)), 'exp': str(int(exp))}
        token = encoder.encode(payload)
        tokens = token.decode().split(".")
        new_token = tokens[0] + "." + tokens[1] + "."
        response = self.client.get('/?token=' + new_token)
        self.assertEquals(200, response.status_code)

if __name__ == '__main__':
    unittest.main()
