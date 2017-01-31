import os
import sys
import time

from structlog import ReturnLoggerFactory
from structlog import configure


def create_payload(user):
    expire_after_seconds = 12 * 60 * 60
    iat = time.time()
    exp = time.time() + expire_after_seconds
    return {
            "user_id": user,
            'iat': str(int(iat)),
            'exp': str(int(exp)),
            "eq_id": '1',
            "period_str": '2016-01-01',
            "period_id": '2016-01-01',
            "form_type": '0205',
            "collection_exercise_sid": "789",
            "ref_p_start_date": "2016-01-01",
            "ref_p_end_date": "2016-09-01",
            "ru_ref": "12346789012A",
            "ru_name": "Apple",
            "return_by": "2016-04-30",
            "employment_date": "2016-06-10",
            "region_code": "GB-GBN"}


def generate_token():
    from app.cryptography.jwt_encoder import Encoder
    encoder = Encoder()
    user = os.getenv('USER', 'UNKNOWN')
    payload = create_payload(user)
    token = encoder.encode(payload)
    encrypted_token = encoder.encrypt_token(token)
    return encrypted_token

if __name__ == '__main__':
    # Disable logging for token generator as url should be only output
    configure(logger_factory=ReturnLoggerFactory())

    if len(sys.argv) > 1:
        print("http://" + sys.argv[1] + "-surveys.eq.ons.digital/session?token=" + generate_token().decode())  # NOQA
    else:
        print("http://localhost:5000/session?token=" + generate_token().decode())  # NOQA
