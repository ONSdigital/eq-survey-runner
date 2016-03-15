from tests.app.authentication.encoder import Encoder
from app.authentication.user import USER_ID, RU_REF, REF_P_START_DATE, REF_P_END_DATE, COLLECTION_EXERCISE_SID, EQ_ID, FORM_TYPE, PERIOD_ID, PERIOD_STR
import os
import time


def create_payload(user):
    iat = time.time()
    exp = time.time() + (5 * 60)
    return {
            USER_ID: user,
            'iat': str(int(iat)),
            'exp': str(int(exp)),
            EQ_ID: '1',
            PERIOD_STR: '2016-01-01',
            PERIOD_ID: '12',
            FORM_TYPE: 'a',
            COLLECTION_EXERCISE_SID: "sid",
            REF_P_START_DATE: "2016-01-01",
            REF_P_END_DATE: "2016-09-01",
            RU_REF: "1234"}


def generate_token():
    encoder = Encoder()
    user = os.getenv('USER', 'UNKNOWN')
    payload = create_payload(user)
    token = encoder.encode(payload)
    encrypted_token = encoder.encrypt(token)
    return encrypted_token

if __name__ == '__main__':
    print("http://localhost:5000/session?token=" + generate_token().decode())  # NOQA
