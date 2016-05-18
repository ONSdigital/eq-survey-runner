from app import settings
from app.authentication.invalid_token_exception import InvalidTokenException
from app.metadata.metadata_store import MetaDataConstants
from app.utilities.strings import to_bytes, to_str
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends.openssl.backend import backend
import logging
import binascii

logger = logging.getLogger(__name__)


class UserIDGenerator(object):

    @staticmethod
    def generate_id(token):
        logger.debug("About to generate a user id")
        ru_ref = token.get(MetaDataConstants.RU_REF)
        collection_exercise_sid = token.get(MetaDataConstants.COLLECTION_EXERCISE_SID)
        eq_id = token.get(MetaDataConstants.EQ_ID)

        if ru_ref and collection_exercise_sid and eq_id:
            logger.debug("Using values %s, %s and %s with a salt", ru_ref, collection_exercise_sid, eq_id)
            salt = to_bytes(settings.EQ_SERVER_SIDE_STORAGE_USER_ID_SALT)
            user_id_material = ru_ref + collection_exercise_sid + eq_id

            kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=settings.EQ_SERVER_SIDE_STORAGE_USER_ID_ITERATIONS, backend=backend)
            generated_user_id = kdf.derive(to_bytes(user_id_material))
            user_id = binascii.hexlify(generated_user_id)
            if settings.EQ_DEV_MODE:
                logger.debug("User ID is %s", to_str(user_id))
            return to_str(user_id)
        else:
            logger.error("Missing values for ru_ref, collection_exercise_sid or eq_id in token %s", token)
            raise InvalidTokenException("Missing values in JWT token")
