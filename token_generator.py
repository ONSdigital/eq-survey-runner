import os
import sys
import time

from app.metadata.metadata_store import MetaDataConstants
from app.dev_mode.jwt_encoder import Encoder


def create_payload(user):
    EXPIRE_AFTER_SECONDS = 12 * 60 * 60
    iat = time.time()
    exp = time.time() + EXPIRE_AFTER_SECONDS
    return {
            MetaDataConstants.USER_ID: user,
            'iat': str(int(iat)),
            'exp': str(int(exp)),
            MetaDataConstants.EQ_ID: '1',
            MetaDataConstants.PERIOD_STR: '2016-01-01',
            MetaDataConstants.PERIOD_ID: '2016-01-01',
            MetaDataConstants.FORM_TYPE: '0205',
            MetaDataConstants.COLLECTION_EXERCISE_SID: "sid",
            MetaDataConstants.REF_P_START_DATE: "2016-01-01",
            MetaDataConstants.REF_P_END_DATE: "2016-09-01",
            MetaDataConstants.RU_REF: "12346789012A",
            MetaDataConstants.RU_NAME: "Apple",
            MetaDataConstants.RETURN_BY: "2016-04-30"}


def generate_token():
    encoder = Encoder()
    user = os.getenv('USER', 'UNKNOWN')
    payload = create_payload(user)
    token = encoder.encode(payload)
    encrypted_token = encoder.encrypt(token)
    return encrypted_token

if __name__ == '__main__':

    if len(sys.argv) > 1:
        print("http://" + sys.argv[1] + "-surveys.eq.ons.digital/session?token=" + generate_token().decode())  # NOQA
    else:
        print("http://localhost:5000/session?token=" + generate_token().decode())  # NOQA
