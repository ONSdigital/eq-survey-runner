import logging
import time
import unittest

from app import create_app
from app import settings
from app.authentication.encoder import Encoder
from app.authentication.user import USER_ID, RU_REF, REF_P_START_DATE, REF_P_END_DATE, COLLECTION_EXERCISE_SID, EQ_ID, FORM_TYPE, PERIOD_ID, PERIOD_STR
from tests.app.authentication import TEST_DO_NOT_USE_RRM_PUBLIC_PEM, TEST_DO_NOT_USE_SR_PRIVATE_PEM


class FlaskClientAuthenticationTestCase(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)

        settings.EQ_RRM_PUBLIC_KEY = TEST_DO_NOT_USE_RRM_PUBLIC_PEM
        settings.EQ_SR_PRIVATE_KEY = TEST_DO_NOT_USE_SR_PRIVATE_PEM

        self.app = create_app("testing")
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
        encrypted_token = encoder.encrypt(token)
        response = self.client.get('/session?token=' + encrypted_token.decode())
        self.assertEquals(302, response.status_code)

    def create_payload(self):
        iat = time.time()
        exp = time.time() + (5 * 60)
        return {
                USER_ID: 'jimmy',
                'iat': str(int(iat)),
                'exp': str(int(exp)),
                EQ_ID: '1',
                PERIOD_STR: '2016-01-01',
                PERIOD_ID: '12',
                FORM_TYPE: '0203',
                COLLECTION_EXERCISE_SID: "sid",
                REF_P_START_DATE: "2016-01-01",
                REF_P_END_DATE: "2016-09-01",
                RU_REF: "1234"}

if __name__ == '__main__':
    unittest.main()
