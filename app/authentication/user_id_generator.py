import binascii
import logging

from cryptography.hazmat.backends.openssl.backend import backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from app import settings
from app.authentication.invalid_token_exception import InvalidTokenException
from app.utilities.strings import to_bytes
from app.utilities.strings import to_str

logger = logging.getLogger(__name__)


class UserIDGenerator(object):

    @staticmethod
    def generate_id(token):
        logger.debug("About to generate a user id")
        collection_exercise_sid, eq_id, form_type, ru_ref = UserIDGenerator._get_token_data(token)

        logger.debug("Using values %s, %s, %s and %s with a salt to generate a user id", ru_ref, collection_exercise_sid, eq_id, form_type)
        salt = to_bytes(settings.EQ_SERVER_SIDE_STORAGE_USER_ID_SALT)
        user_id = UserIDGenerator._generate(collection_exercise_sid, eq_id, form_type, ru_ref, salt)
        if settings.EQ_DEV_MODE:
            logger.debug("User ID is %s", to_str(user_id))
        return to_str(user_id)

    @staticmethod
    def generate_ik(token):
        logger.debug("About to generate a user ignition key")
        collection_exercise_sid, eq_id, form_type, ru_ref = UserIDGenerator._get_token_data(token)
        logger.debug("Using values %s, %s, %s and %s with a salt to generate a user ik", ru_ref, collection_exercise_sid, eq_id, form_type)
        salt = to_bytes(settings.EQ_SERVER_SIDE_STORAGE_USER_IK_SALT)
        ik = UserIDGenerator._generate(collection_exercise_sid, eq_id, form_type, ru_ref, salt)
        if settings.EQ_DEV_MODE:
            logger.debug("User IK is %s", to_str(ik))
        return to_str(ik)

    @staticmethod
    def _generate(collection_exercise_sid, eq_id, form_type, ru_ref, salt):
        key_material = ru_ref + collection_exercise_sid + eq_id + form_type
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt,
                         iterations=settings.EQ_SERVER_SIDE_STORAGE_USER_ID_ITERATIONS, backend=backend)
        generated_key = kdf.derive(to_bytes(key_material))
        return binascii.hexlify(generated_key)

    @staticmethod
    def _get_token_data(token):
        ru_ref = token.get("ru_ref")
        collection_exercise_sid = token.get("collection_exercise_sid")
        eq_id = token.get("eq_id")
        form_type = token.get("form_type")

        if ru_ref and collection_exercise_sid and eq_id and form_type:
            return collection_exercise_sid, eq_id, form_type, ru_ref
        else:
            logger.error("Missing values for ru_ref, collection_exercise_sid, form_type or eq_id in token %s", token)
            raise InvalidTokenException("Missing values in JWT token")
