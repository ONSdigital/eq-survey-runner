import json

from jwcrypto import jwe, jwt
from jwcrypto.common import base64url_decode
from jwcrypto.jwe import InvalidJWEData
from jwcrypto.jws import InvalidJWSSignature, InvalidJWSObject
from jwcrypto.jwt import JWTInvalidClaimFormat, JWTMissingClaim, JWTExpired

from app.authentication.invalid_token_exception import InvalidTokenException


def decrypt_jwe(encrypted_token, secret_store, purpose, default_kid=None):
    try:
        jwe_token = jwe.JWE(algs=['RSA-OAEP', 'A256GCM'])
        jwe_token.deserialize(encrypted_token)

        try:
            jwe_kid = extract_kid_from_header(encrypted_token)
        except InvalidTokenException as e:
            if default_kid:
                jwe_kid = default_kid
            else:
                raise e

        private_jwk = secret_store.get_private_key_by_kid(purpose, jwe_kid).as_jwk()

        jwe_token.decrypt(private_jwk)

        return jwe_token.payload.decode()
    except InvalidJWEData as e:
        raise InvalidTokenException(repr(e))


def encrypt_jwe(payload, kid, secret_store, purpose, alg="RSA-OAEP", enc="A256GCM"):

    public_jwk = secret_store.get_public_key_by_kid(purpose, kid).as_jwk()

    protected_header = {
        "alg": alg,
        "enc": enc,
        "kid": kid,
    }

    token = jwe.JWE(plaintext=payload, protected=protected_header)

    token.add_recipient(public_jwk)

    return token.serialize(compact=True)


def decode_jwt(jwt_token, secret_store, purpose, leeway=None):
    try:
        jwt_kid = extract_kid_from_header(jwt_token)

        public_jwk = secret_store.get_public_key_by_kid(purpose, jwt_kid).as_jwk()

        check_claims = {
            "exp": None,
            "iat": None,
        }

        signed_token = jwt.JWT(algs=['RS256'], check_claims=check_claims)

        if leeway:
            signed_token.leeway = leeway

        signed_token.deserialize(jwt_token, key=public_jwk)

        return json.loads(signed_token.claims)
    except (InvalidJWSObject,
            InvalidJWSSignature,
            JWTInvalidClaimFormat,
            JWTMissingClaim,
            JWTExpired,
            ValueError) as e:
        raise InvalidTokenException(repr(e))


def encode_jwt(claims, kid, secret_store, purpose):
    private_jwk = secret_store.get_private_key_by_kid(purpose, kid).as_jwk()

    header = {
        'kid': kid,
        'typ': 'jwt',
        'alg': 'RS256',
    }
    token = jwt.JWT(claims=claims, header=header)

    token.make_signed_token(private_jwk)

    return token.serialize()


def extract_kid_from_header(token):
    header = token.split('.')[:1][0]

    if header is "":
        raise InvalidTokenException("Missing Headers")

    try:
        protected_header = base64url_decode(header).decode()

        protected_header_data = json.loads(protected_header)

        if 'kid' in protected_header:
            return protected_header_data['kid']
    except ValueError:
        raise InvalidTokenException("Invalid Header")

    raise InvalidTokenException("Missing kid")
