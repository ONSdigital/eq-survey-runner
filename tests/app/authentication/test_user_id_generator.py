import unittest
from sdc.crypto.exceptions import InvalidTokenException

from app import settings
from app.authentication.user_id_generator import UserIDGenerator


class TestUserIDGenerator(unittest.TestCase):
    def setUp(self):
        settings.EQ_SERVER_SIDE_STORAGE = True
        self._iterations = 1000

    def test_generate_id(self):
        id_generator = UserIDGenerator(self._iterations, '', '')
        user_id_1 = id_generator.generate_id(self.create_token('1', '2', '3', '4'))
        user_id_2 = id_generator.generate_id(self.create_token('1', '2', '3', '4'))
        user_id_3 = id_generator.generate_id(self.create_token('1', '2', '4', '4'))
        user_id_4 = id_generator.generate_id(self.create_token('2', '2', '3', '4'))
        user_id_5 = id_generator.generate_id(self.create_token('1', '1', '3', '4'))
        user_id_6 = id_generator.generate_id(self.create_token('2', '2', '4', '4'))
        user_id_7 = id_generator.generate_id(self.create_token('2', '2', '4', '5'))
        user_id_8 = id_generator.generate_id(self.create_token('1', '2', '3', '5'))

        self.assertEqual(user_id_1, user_id_2)

        self.assertNotEqual(user_id_1, user_id_3)
        self.assertNotEqual(user_id_1, user_id_3)
        self.assertNotEqual(user_id_1, user_id_4)
        self.assertNotEqual(user_id_1, user_id_5)
        self.assertNotEqual(user_id_1, user_id_6)
        self.assertNotEqual(user_id_1, user_id_7)
        self.assertNotEqual(user_id_1, user_id_8)

    def test_different_salt_creates_different_user_id(self):
        id_generator_1 = UserIDGenerator(self._iterations, '', '')
        user_id_1 = id_generator_1.generate_id(self.create_token('1', '2', '3', '4'))

        id_generator_2 = UserIDGenerator(self._iterations, 'random', '')
        user_id_2 = id_generator_2.generate_id(self.create_token('1', '2', '3', '4'))

        self.assertNotEqual(user_id_1, user_id_2)

    def test_generate_ik(self):
        id_generator = UserIDGenerator(self._iterations, '', '')
        user_ik_1 = id_generator.generate_ik(self.create_token('1', '2', '3', '4'))
        user_ik_2 = id_generator.generate_ik(self.create_token('1', '2', '3', '4'))
        user_ik_3 = id_generator.generate_ik(self.create_token('1', '2', '4', '4'))
        user_ik_4 = id_generator.generate_ik(self.create_token('2', '2', '3', '4'))
        user_ik_5 = id_generator.generate_ik(self.create_token('1', '1', '3', '4'))
        user_ik_6 = id_generator.generate_ik(self.create_token('2', '2', '4', '4'))
        user_ik_7 = id_generator.generate_ik(self.create_token('2', '2', '4', '5'))
        user_ik_8 = id_generator.generate_ik(self.create_token('1', '2', '3', '5'))

        self.assertEqual(user_ik_1, user_ik_2)

        self.assertNotEqual(user_ik_1, user_ik_3)
        self.assertNotEqual(user_ik_1, user_ik_3)
        self.assertNotEqual(user_ik_1, user_ik_4)
        self.assertNotEqual(user_ik_1, user_ik_5)
        self.assertNotEqual(user_ik_1, user_ik_6)
        self.assertNotEqual(user_ik_1, user_ik_7)
        self.assertNotEqual(user_ik_1, user_ik_8)

    def test_different_salt_creates_different_user_ik(self):
        id_generator_1 = UserIDGenerator(self._iterations, '', '')
        user_ik_1 = id_generator_1.generate_ik(self.create_token('1', '2', '3', '4'))

        id_generator_2 = UserIDGenerator(self._iterations, '', 'random')
        user_ik_2 = id_generator_2.generate_ik(self.create_token('1', '2', '3', '4'))

        self.assertNotEqual(user_ik_1, user_ik_2)

    def test_generate_id_throws_invalid_token_exception(self):
        id_generator = UserIDGenerator(self._iterations, '', '')

        with self.assertRaises(InvalidTokenException):
            id_generator.generate_id(self.create_token('1', '2', None, '4'))
        with self.assertRaises(InvalidTokenException):
            id_generator.generate_id(self.create_token('1', None, '3', '4'))
        with self.assertRaises(InvalidTokenException):
            id_generator.generate_id(self.create_token(None, '2', '3', '4'))
        with self.assertRaises(InvalidTokenException):
            id_generator.generate_id(self.create_token(None, None, None, '4'))
        with self.assertRaises(InvalidTokenException):
            id_generator.generate_id(self.create_token(None, None, None, None))

    def test_generate_ik_throws_invalid_token_exception(self):
        id_generator = UserIDGenerator(self._iterations, '', '')

        with self.assertRaises(InvalidTokenException):
            id_generator.generate_ik(self.create_token('1', '2', None, '4'))
        with self.assertRaises(InvalidTokenException):
            id_generator.generate_ik(self.create_token('1', None, '3', '4'))
        with self.assertRaises(InvalidTokenException):
            id_generator.generate_ik(self.create_token(None, '2', '3', '4'))
        with self.assertRaises(InvalidTokenException):
            id_generator.generate_ik(self.create_token(None, None, None, '4'))
        with self.assertRaises(InvalidTokenException):
            id_generator.generate_ik(self.create_token(None, None, None, None))

    @staticmethod
    def create_token(eq_id, collection_exercise_sid, ru_ref, form_type):
        return {
            'eq_id': eq_id,
            'collection_exercise_sid': collection_exercise_sid,
            'ru_ref': ru_ref,
            'form_type': form_type}

    def test_generate_id_no_metadata_raises_error(self):
        id_generator = UserIDGenerator(self._iterations, '', '')
        self.assertRaises(ValueError, id_generator.generate_id, None)

    def test_generate_ik_no_token_raises_error(self):
        id_generator = UserIDGenerator(self._iterations, '', '')
        self.assertRaises(ValueError, id_generator.generate_ik, None)

    def test_create_generator_no_user_id_salt_raises_error(self):
        with self.assertRaises(ValueError):
            UserIDGenerator(self._iterations, None, '')

    def test_create_generator_no_user_ik_salt_raises_error(self):
        with self.assertRaises(ValueError):
            UserIDGenerator(self._iterations, '', None)

if __name__ == '__main__':
    unittest.main()
