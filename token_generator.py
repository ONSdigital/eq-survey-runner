import os
import sys
import time

from app.dev_mode.jwt_encoder import Encoder
from app.metadata.metadata_store import MetaDataConstants


def create_payload(user):
    expire_after_seconds = 12 * 60 * 60
    iat = time.time()
    exp = time.time() + expire_after_seconds
    return {
            MetaDataConstants.USER_ID.claim_id: user,
            'iat': str(int(iat)),
            'exp': str(int(exp)),
            MetaDataConstants.EQ_ID.claim_id: '1',
            MetaDataConstants.PERIOD_STR.claim_id: '2016-01-01',
            MetaDataConstants.PERIOD_ID.claim_id: '2016-01-01',
            MetaDataConstants.FORM_TYPE.claim_id: '0205',
            MetaDataConstants.COLLECTION_EXERCISE_SID.claim_id: "789",
            MetaDataConstants.REF_P_START_DATE.claim_id: "2016-01-01",
            MetaDataConstants.REF_P_END_DATE.claim_id: "2016-09-01",
            MetaDataConstants.RU_REF.claim_id: "12346789012A",
            MetaDataConstants.RU_NAME.claim_id: "Apple",
            MetaDataConstants.RETURN_BY.claim_id: "2016-04-30",
            MetaDataConstants.EMPLOYMENT_DATE.claim_id: "2016-06-10"}


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
