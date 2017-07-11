from app.cryptography.token_helper import encode_jwt, encrypt_jwe
from app.secrets import KEY_PURPOSE_SUBMISSION


def encrypt(json, secret_store):

    jwt_key = secret_store.get_key_for_purpose_and_type(KEY_PURPOSE_SUBMISSION, "private")

    payload = encode_jwt(json, jwt_key.kid, secret_store, KEY_PURPOSE_SUBMISSION)

    jwe_key = secret_store.get_key_for_purpose_and_type(KEY_PURPOSE_SUBMISSION, "public")

    return encrypt_jwe(payload, jwe_key.kid, secret_store, KEY_PURPOSE_SUBMISSION)
