from app.authentication.user_id_generator import UserIDGenerator
from app.metadata.metadata_store import MetaDataConstants
from app import settings
import unittest


class TestUserIDGenerator(unittest.TestCase):

    def setUp(self):
        settings.EQ_SERVER_SIDE_STORAGE = True

    def test_generate_id(self):
        user_id_1 = UserIDGenerator.generate_id(self.create_token('1', '2', '3'))
        user_id_2 = UserIDGenerator.generate_id(self.create_token('1', '2', '3'))
        user_id_3 = UserIDGenerator.generate_id(self.create_token('1', '2', '4'))
        self.assertEqual(user_id_1, user_id_2)
        self.assertNotEquals(user_id_1, user_id_3)
        self.assertNotEquals(user_id_2, user_id_3)

    def create_token(self, eq_id, collection_exercise_sid, ru_ref):
        return {
                MetaDataConstants.EQ_ID: eq_id,
                MetaDataConstants.COLLECTION_EXERCISE_SID: collection_exercise_sid,
                MetaDataConstants.RU_REF: ru_ref}
