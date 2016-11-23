import unittest

from app import settings
from app.authentication.invalid_token_exception import InvalidTokenException
from app.authentication.user_id_generator import UserIDGenerator


class TestUserIDGenerator(unittest.TestCase):

    def setUp(self):
        settings.EQ_SERVER_SIDE_STORAGE = True

    def test_generate_id(self):
        user_id_1 = UserIDGenerator.generate_id(self.create_token('1', '2', '3', '4'))
        user_id_2 = UserIDGenerator.generate_id(self.create_token('1', '2', '3', '4'))
        user_id_3 = UserIDGenerator.generate_id(self.create_token('1', '2', '4', '4'))
        user_id_4 = UserIDGenerator.generate_id(self.create_token('2', '2', '3', '4'))
        user_id_5 = UserIDGenerator.generate_id(self.create_token('1', '1', '3', '4'))
        user_id_6 = UserIDGenerator.generate_id(self.create_token('2', '2', '4', '4'))
        user_id_7 = UserIDGenerator.generate_id(self.create_token('2', '2', '4', '5'))
        user_id_8 = UserIDGenerator.generate_id(self.create_token('1', '2', '3', '5'))

        self.assertEqual(user_id_1, user_id_2)

        self.assertNotEquals(user_id_1, user_id_3)
        self.assertNotEquals(user_id_1, user_id_3)
        self.assertNotEquals(user_id_1, user_id_4)
        self.assertNotEquals(user_id_1, user_id_5)
        self.assertNotEquals(user_id_1, user_id_6)
        self.assertNotEquals(user_id_1, user_id_7)
        self.assertNotEquals(user_id_1, user_id_8)

    def test_different_salt_creates_different_userids(self):
        user_id_1 = UserIDGenerator.generate_id(self.create_token('1', '2', '3', '4'))
        settings.EQ_SERVER_SIDE_STORAGE_USER_ID_SALT = "random"
        user_id_2 = UserIDGenerator.generate_id(self.create_token('1', '2', '3', '4'))
        self.assertNotEqual(user_id_1, user_id_2)

    def test_generate_ik(self):
        user_ik_1 = UserIDGenerator.generate_ik(self.create_token('1', '2', '3', '4'))
        user_ik_2 = UserIDGenerator.generate_ik(self.create_token('1', '2', '3', '4'))
        user_ik_3 = UserIDGenerator.generate_ik(self.create_token('1', '2', '4', '4'))
        user_ik_4 = UserIDGenerator.generate_ik(self.create_token('2', '2', '3', '4'))
        user_ik_5 = UserIDGenerator.generate_ik(self.create_token('1', '1', '3', '4'))
        user_ik_6 = UserIDGenerator.generate_ik(self.create_token('2', '2', '4', '4'))
        user_ik_7 = UserIDGenerator.generate_ik(self.create_token('2', '2', '4', '5'))
        user_ik_8 = UserIDGenerator.generate_ik(self.create_token('1', '2', '3', '5'))

        self.assertEqual(user_ik_1, user_ik_2)

        self.assertNotEquals(user_ik_1, user_ik_3)
        self.assertNotEquals(user_ik_1, user_ik_3)
        self.assertNotEquals(user_ik_1, user_ik_4)
        self.assertNotEquals(user_ik_1, user_ik_5)
        self.assertNotEquals(user_ik_1, user_ik_6)
        self.assertNotEquals(user_ik_1, user_ik_7)
        self.assertNotEquals(user_ik_1, user_ik_8)

    def test_different_salt_creates_different_useriks(self):
        user_id_1 = UserIDGenerator.generate_ik(self.create_token('1', '2', '3', '4'))
        settings.EQ_SERVER_SIDE_STORAGE_USER_IK_SALT = "random"
        user_id_2 = UserIDGenerator.generate_ik(self.create_token('1', '2', '3', '4'))
        self.assertNotEqual(user_id_1, user_id_2)

    def test_generate_id_throws_invalid_token_exception(self):
        with self.assertRaises(InvalidTokenException):
            UserIDGenerator.generate_id(self.create_token('1', '2', None, '4'))
        with self.assertRaises(InvalidTokenException):
            UserIDGenerator.generate_id(self.create_token('1', None, '3', '4'))
        with self.assertRaises(InvalidTokenException):
            UserIDGenerator.generate_id(self.create_token(None, '2', '3', '4'))
        with self.assertRaises(InvalidTokenException):
            UserIDGenerator.generate_id(self.create_token(None, None, None, '4'))
        with self.assertRaises(InvalidTokenException):
            UserIDGenerator.generate_id(self.create_token(None, None, None, None))

    def test_generate_ik_throws_invalid_token_exception(self):
        with self.assertRaises(InvalidTokenException):
            UserIDGenerator.generate_ik(self.create_token('1', '2', None, '4'))
        with self.assertRaises(InvalidTokenException):
            UserIDGenerator.generate_ik(self.create_token('1', None, '3', '4'))
        with self.assertRaises(InvalidTokenException):
            UserIDGenerator.generate_ik(self.create_token(None, '2', '3', '4'))
        with self.assertRaises(InvalidTokenException):
            UserIDGenerator.generate_ik(self.create_token(None, None, None, '4'))
        with self.assertRaises(InvalidTokenException):
            UserIDGenerator.generate_ik(self.create_token(None, None, None, None))

    @staticmethod
    def create_token(eq_id, collection_exercise_sid, ru_ref, form_type):
        return {
                "eq_id": eq_id,
                "collection_exercise_sid": collection_exercise_sid,
                "ru_ref": ru_ref,
                "form_type": form_type}

if __name__ == '__main__':
    unittest.main()
