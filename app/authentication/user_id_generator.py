import binascii

from cryptography.hazmat.backends.openssl.backend import backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from structlog import get_logger

from app import settings
from app.authentication.invalid_token_exception import InvalidTokenException
from app.utilities.strings import to_bytes
from app.utilities.strings import to_str

logger = get_logger()


class UserIDGenerator(object):

    @staticmethod
    def generate_id(metadata):
        collection_exercise_sid, eq_id, form_type, ru_ref = UserIDGenerator._get_token_data(metadata)

        logger.debug("generating user id", ru_ref=ru_ref, ce_id=collection_exercise_sid, eq_id=eq_id, form_type=form_type)
        salt = to_bytes(settings.EQ_SERVER_SIDE_STORAGE_USER_ID_SALT)
        user_id = UserIDGenerator._generate(collection_exercise_sid, eq_id, form_type, ru_ref, salt)
        return to_str(user_id)

    @staticmethod
    def generate_ik(token):
        collection_exercise_sid, eq_id, form_type, ru_ref = UserIDGenerator._get_token_data(token)
        logger.debug("generating user ik", ru_ref=ru_ref, ce_id=collection_exercise_sid, eq_id=eq_id, form_type=form_type)
        salt = to_bytes(settings.EQ_SERVER_SIDE_STORAGE_USER_IK_SALT)
        ik = UserIDGenerator._generate(collection_exercise_sid, eq_id, form_type, ru_ref, salt)
        return to_str(ik)

    @staticmethod
    def _generate(collection_exercise_sid, eq_id, form_type, ru_ref, salt):
        key_material = ru_ref + collection_exercise_sid + eq_id + form_type
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt,
                         iterations=settings.EQ_SERVER_SIDE_STORAGE_USER_ID_ITERATIONS, backend=backend)
        generated_key = kdf.derive(to_bytes(key_material))
        return binascii.hexlify(generated_key)

    @staticmethod
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
