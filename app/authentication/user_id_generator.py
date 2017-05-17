import binascii

from cryptography.hazmat.backends.openssl.backend import backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from structlog import get_logger

from app.authentication.invalid_token_exception import InvalidTokenException
from app.utilities.strings import to_bytes
from app.utilities.strings import to_str

logger = get_logger()


class UserIDGenerator(object):

    def __init__(self, user_id_salt, user_ik_salt, user_id_iterations):
        super().__init__()
        self._user_id_salt = user_id_salt
        self._user_ik_salt = user_ik_salt
        self._user_id_iterations = user_id_iterations

    def generate_id(self, metadata):
        # pylint: disable=maybe-no-member
        collection_exercise_sid, eq_id, form_type, ru_ref = _get_token_data(metadata)

        logger.debug("generating user id", ru_ref=ru_ref, ce_id=collection_exercise_sid, eq_id=eq_id, form_type=form_type)
        salt = to_bytes(self._user_id_salt)
        user_id = self._generate(collection_exercise_sid, eq_id, form_type, ru_ref, salt)
        return to_str(user_id)

    def generate_ik(self, token):
        # pylint: disable=maybe-no-member
        collection_exercise_sid, eq_id, form_type, ru_ref = _get_token_data(token)
        logger.debug("generating user ik", ru_ref=ru_ref, ce_id=collection_exercise_sid, eq_id=eq_id, form_type=form_type)
        salt = to_bytes(self._user_ik_salt)
        ik = self._generate(collection_exercise_sid, eq_id, form_type, ru_ref, salt)
        return to_str(ik)

    def _generate(self, collection_exercise_sid, eq_id, form_type, ru_ref, salt):
        key_material = ru_ref + collection_exercise_sid + eq_id + form_type
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt,
                         iterations=self._user_id_iterations, backend=backend)
        generated_key = kdf.derive(to_bytes(key_material))
        return binascii.hexlify(generated_key)


def _get_token_data(metadata):
    ru_ref = metadata.get("ru_ref")
    collection_exercise_sid = metadata.get("collection_exercise_sid")
    eq_id = metadata.get("eq_id")
    form_type = metadata.get("form_type")

    if ru_ref and collection_exercise_sid and eq_id and form_type:
        return collection_exercise_sid, eq_id, form_type, ru_ref
    else:
        logger.error("missing values for ru_ref, collection_exercise_sid, form_type or eq_id", metadata=metadata)
        raise InvalidTokenException("Missing values in JWT token")
