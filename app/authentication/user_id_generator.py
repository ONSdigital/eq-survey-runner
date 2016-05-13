from app import settings
from app.metadata.metadata_store import MetaDataConstants
from app.utilities.strings import to_str
import hashlib
import logging

logger = logging.getLogger(__name__)


class UserIDGenerator(object):

    @staticmethod
    def generate_id(token):
        logger.debug("About to generate a user id")
        ru_ref = token.get(MetaDataConstants.RU_REF)
        collection_exercise_sid = token.get(MetaDataConstants.COLLECTION_EXERCISE_SID)
        eq_id = token.get(MetaDataConstants.EQ_ID)

        logger.debug("Using values %s, %s and %s with a salt", ru_ref, collection_exercise_sid, eq_id)
        salt = settings.EQ_SERVER_SIDE_STORAGE_SALT

        sha256 = hashlib.sha256()
        sha256.update(to_str(ru_ref).encode('utf-8'))
        sha256.update(to_str(collection_exercise_sid).encode('utf-8'))
        sha256.update(to_str(eq_id).encode('utf-8'))
        sha256.update(to_str(salt).encode('utf-8'))

        user_id = sha256.hexdigest()
        logger.debug("User ID is %s", user_id)
        return user_id
