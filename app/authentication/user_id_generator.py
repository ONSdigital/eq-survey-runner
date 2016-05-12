from app import settings
import hashlib


class UserIDGenerator(object):

    @staticmethod
    def generate_id(metadata_store):
        ru_ref = metadata_store.get_ru_ref()
        collection_exercise_sid = metadata_store.get_collection_exercise_sid()
        eq_id = metadata_store.get_eq_id()
        salt = settings.EQ_SERVER_SIDE_STORAGE_SALT

        sha256 = hashlib.sha256()
        sha256.update(ru_ref)
        sha256.update(collection_exercise_sid)
        sha256.update(eq_id)
        sha256.update(salt)

        return sha256.hexdigest()
