import logging
import time
import unittest

from app import create_app
from app import settings
from app.dev_mode.jwt_encoder import Encoder
from tests.app.authentication import TEST_DO_NOT_USE_RRM_PUBLIC_PEM, TEST_DO_NOT_USE_SR_PRIVATE_PEM


class FlaskClientAuthenticationTestCase(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)

        settings.EQ_USER_AUTHENTICATION_RRM_PUBLIC_KEY = TEST_DO_NOT_USE_RRM_PUBLIC_PEM
        settings.EQ_USER_AUTHENTICATION_SR_PRIVATE_KEY = TEST_DO_NOT_USE_SR_PRIVATE_PEM

        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=False)

    def tearDown(self):
        self.app_context.pop()

    def test_no_token(self):
        response = self.client.get('/session')
        self.assertEquals(401, response.status_code)

    def test_invalid_token(self):
        token = "invalid"
        response = self.client.get('/session?token=' + token)
        self.assertEquals(403, response.status_code)

    def test_fully_encrypted(self):
        encoder = Encoder()
        payload = self.create_payload()
        token = encoder.encode(payload)
        encrypted_token = encoder.encrypt_token(token)
        response = self.client.get('/session?token=' + encrypted_token.decode())
        self.assertEquals(302, response.status_code)

    @staticmethod
    def create_payload():
        iat = time.time()
        exp = time.time() + (5 * 60)
        return {
                "user_id": 'jimmy',
                'iat': str(int(iat)),
                'exp': str(int(exp)),
                "eq_id": '1',
                "period_str": '2016-01-01',
                "period_id": '12',
                "form_type": '0203',
                "collection_exercise_sid": "sid",
                "ref_p_start_date": "2016-01-01",
                "ref_p_end_date": "2016-09-01",
                "ru_ref": "1234",
                "ru_name": "Test",
                "return_by": "2016-09-09"}

if __name__ == '__main__':
    unittest.main()
