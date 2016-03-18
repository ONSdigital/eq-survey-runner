import os
import sys
import time

from app.authentication.encoder import Encoder
from app.authentication.user import UserConstants


def create_payload(user):
    iat = time.time()
    exp = time.time() + (5 * 60 * 60)
    return {
            UserConstants.USER_ID: user,
            'iat': str(int(iat)),
            'exp': str(int(exp)),
            UserConstants.EQ_ID: '1',
            UserConstants.PERIOD_STR: '2016-01-01',
            UserConstants.PERIOD_ID: '2016-01-01',
            UserConstants.FORM_TYPE: '0205',
            UserConstants.COLLECTION_EXERCISE_SID: "sid",
            UserConstants.REF_P_START_DATE: "2016-01-01",
            UserConstants.REF_P_END_DATE: "2016-09-01",
            UserConstants.RU_REF: "12346789012A",
            UserConstants.RU_NAME: "Apple",
            UserConstants.RETURN_BY: "2016-04-30"}


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
