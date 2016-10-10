import os
import sys
import time

from app.dev_mode.jwt_encoder import Encoder
from app.parser.metadata_parser import MetadataConstants


def create_payload(user):
    expire_after_seconds = 12 * 60 * 60
    iat = time.time()
    exp = time.time() + expire_after_seconds
    return {
            MetadataConstants.USER_ID.claim_id: user,
            'iat': str(int(iat)),
            'exp': str(int(exp)),
            MetadataConstants.EQ_ID.claim_id: '1',
            MetadataConstants.PERIOD_STR.claim_id: '2016-01-01',
            MetadataConstants.PERIOD_ID.claim_id: '2016-01-01',
            MetadataConstants.FORM_TYPE.claim_id: '0205',
            MetadataConstants.COLLECTION_EXERCISE_SID.claim_id: "789",
            MetadataConstants.REF_P_START_DATE.claim_id: "2016-01-01",
            MetadataConstants.REF_P_END_DATE.claim_id: "2016-09-01",
            MetadataConstants.RU_REF.claim_id: "12346789012A",
            MetadataConstants.RU_NAME.claim_id: "Apple",
            MetadataConstants.RETURN_BY.claim_id: "2016-04-30",
            MetadataConstants.EMPLOYMENT_DATE.claim_id: "2016-06-10"}


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
