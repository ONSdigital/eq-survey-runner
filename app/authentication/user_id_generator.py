import binascii

from cryptography.hazmat.backends.openssl.backend import backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from structlog import get_logger

from sdc.crypto.exceptions import InvalidTokenException
from app.utilities.strings import to_bytes
from app.utilities.strings import to_str

logger = get_logger()


class UserIDGenerator:

    def __init__(self, iterations, user_id_salt, user_ik_salt):
        if user_id_salt is None:
            raise ValueError('user_id_salt is required')
        if user_ik_salt is None:
            raise ValueError('user_ik_salt is required')

        self._iterations = iterations
        self._user_id_salt = user_id_salt
        self._user_ik_salt = user_ik_salt

    def generate_id(self, metadata):
        if metadata is None:
            raise ValueError('metadata is required')

        collection_exercise_sid, eq_id, form_type, ru_ref = UserIDGenerator._get_token_data(metadata)
        logger.debug('generating user id', ru_ref=ru_ref, ce_id=collection_exercise_sid, eq_id=eq_id, form_type=form_type)
        salt = to_bytes(self._user_id_salt)
        user_id = self._generate(collection_exercise_sid, eq_id, form_type, ru_ref, salt)
        return to_str(user_id)

    def generate_ik(self, token):
        if token is None:
            raise ValueError('token is required')

        collection_exercise_sid, eq_id, form_type, ru_ref = UserIDGenerator._get_token_data(token)
        logger.debug('generating user ik', ru_ref=ru_ref, ce_id=collection_exercise_sid, eq_id=eq_id, form_type=form_type)
        salt = to_bytes(self._user_ik_salt)
        ik = self._generate(collection_exercise_sid, eq_id, form_type, ru_ref, salt)
        return to_str(ik)

    def _generate(self, collection_exercise_sid, eq_id, form_type, ru_ref, salt):
        key_material = ru_ref + collection_exercise_sid + eq_id + form_type
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt,
                         iterations=self._iterations, backend=backend)
        generated_key = kdf.derive(to_bytes(key_material))
        return binascii.hexlify(generated_key)

    @staticmethod
    def _get_token_data(metadata):
        ru_ref = metadata.get('ru_ref')
        collection_exercise_sid = metadata.get('collection_exercise_sid')
        eq_id = metadata.get('eq_id')
        form_type = metadata.get('form_type')

        if ru_ref and collection_exercise_sid and eq_id and form_type:
            return collection_exercise_sid, eq_id, form_type, ru_ref

        logger.error('missing values for ru_ref, collection_exercise_sid, form_type or eq_id', metadata=metadata)
        raise InvalidTokenException('Missing values in JWT token')
