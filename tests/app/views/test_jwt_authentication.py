import logging
import time
import unittest

from app import create_app
from app import settings
from app.data_model.metadata_store import MetaDataConstants
from app.dev_mode.jwt_encoder import Encoder
from tests.app.authentication import TEST_DO_NOT_USE_RRM_PUBLIC_PEM, TEST_DO_NOT_USE_SR_PRIVATE_PEM


class FlaskClientAuthenticationTestCase(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)

        settings.EQ_USER_AUTHENTICATION_RRM_PUBLIC_KEY = TEST_DO_NOT_USE_RRM_PUBLIC_PEM
        settings.EQ_USER_AUTHENTICATION_SR_PRIVATE_KEY = TEST_DO_NOT_USE_SR_PRIVATE_PEM

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
                MetaDataConstants.USER_ID.claim_id: 'jimmy',
                'iat': str(int(iat)),
                'exp': str(int(exp)),
                MetaDataConstants.EQ_ID.claim_id: '1',
                MetaDataConstants.PERIOD_STR.claim_id: '2016-01-01',
                MetaDataConstants.PERIOD_ID.claim_id: '12',
                MetaDataConstants.FORM_TYPE.claim_id: '0203',
                MetaDataConstants.COLLECTION_EXERCISE_SID.claim_id: "sid",
                MetaDataConstants.REF_P_START_DATE.claim_id: "2016-01-01",
                MetaDataConstants.REF_P_END_DATE.claim_id: "2016-09-01",
                MetaDataConstants.RU_REF.claim_id: "1234",
                MetaDataConstants.RU_NAME.claim_id: "Test",
                MetaDataConstants.RETURN_BY.claim_id: "2016-09-09"}

if __name__ == '__main__':
    unittest.main()
