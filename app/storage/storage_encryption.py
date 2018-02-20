import hashlib

from jwcrypto import jwe, jwk
from jwcrypto.common import base64url_encode, base64url_decode
from structlog import get_logger
import simplejson as json

from app.utilities.strings import to_bytes
from app.utilities.strings import to_str

logger = get_logger()


class StorageEncryption:

    def __init__(self, user_id, user_ik, pepper):
        if user_id is None:
            raise ValueError('User id must be set')
        if user_ik is None:
            raise ValueError('User ik must be set')
        if pepper is None:
            raise ValueError('Pepper must be set')

        self.key = self._generate_key(user_id, user_ik, pepper)

    @staticmethod
    def _generate_key(user_id, user_ik, pepper):
        sha256 = hashlib.sha256()
        sha256.update(to_str(user_id).encode('utf-8'))
        sha256.update(to_str(user_ik).encode('utf-8'))
        sha256.update(to_str(pepper).encode('utf-8'))

        # we only need the first 32 characters for the CEK
        cek = to_bytes(sha256.hexdigest()[:32])

        password = {
            'kty': 'oct',
            'k': base64url_encode(cek),
        }

        return jwk.JWK(**password)

    def encrypt_data(self, data):
        if not isinstance(data, str):
            data = json.dumps(data)

        protected_header = {
            'alg': 'dir',
            'enc': 'A256GCM',
            'kid': '1,1',
        }

        jwe_token = jwe.JWE(plaintext=base64url_encode(data), protected=protected_header)

        jwe_token.add_recipient(self.key)

        return jwe_token.serialize(compact=True)

    def decrypt_data(self, encrypted_token):

        jwe_token = jwe.JWE(algs=['dir', 'A256GCM'])
        jwe_token.deserialize(encrypted_token, self.key)

        return base64url_decode(jwe_token.payload.decode()).decode()
