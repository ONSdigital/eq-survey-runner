import unittest

from app import settings
from app.authentication.user_id_generator import UserIDGenerator


class TestUserIDGenerator(unittest.TestCase):
    def setUp(self):
        settings.EQ_SERVER_SIDE_STORAGE = True
        self._iterations = 1000

    def test_generate_id(self):
        id_generator = UserIDGenerator(self._iterations, '', '')
        user_id_1 = id_generator.generate_id('1234567890123456')
        user_id_2 = id_generator.generate_id('1234567890123456')
        user_id_3 = id_generator.generate_id('0000000000000000')

        self.assertEqual(user_id_1, user_id_2)
        self.assertNotEqual(user_id_1, user_id_3)

    def test_different_salt_creates_different_user_id(self):
        id_generator_1 = UserIDGenerator(self._iterations, '', '')
        user_id_1 = id_generator_1.generate_id('1234567890123456')

        id_generator_2 = UserIDGenerator(self._iterations, 'random', '')
        user_id_2 = id_generator_2.generate_id('1234567890123456')

        self.assertNotEqual(user_id_1, user_id_2)

    def test_generate_ik(self):
        id_generator = UserIDGenerator(self._iterations, '', '')
        user_ik_1 = id_generator.generate_ik('1234567890123456')
        user_ik_2 = id_generator.generate_ik('1234567890123456')
        user_ik_3 = id_generator.generate_ik('1111111111111111')

        self.assertEqual(user_ik_1, user_ik_2)
        self.assertNotEqual(user_ik_1, user_ik_3)

    def test_different_salt_creates_different_user_ik(self):
        id_generator_1 = UserIDGenerator(self._iterations, '', '')
        user_ik_1 = id_generator_1.generate_ik('1234567890123456')

        id_generator_2 = UserIDGenerator(self._iterations, '', 'random')
        user_ik_2 = id_generator_2.generate_ik('1234567890123456')

        self.assertNotEqual(user_ik_1, user_ik_2)

    def test_create_generator_no_user_id_salt_raises_error(self):
        with self.assertRaises(ValueError):
            UserIDGenerator(self._iterations, None, '')

    def test_create_generator_no_user_ik_salt_raises_error(self):
        with self.assertRaises(ValueError):
            UserIDGenerator(self._iterations, '', None)


if __name__ == '__main__':
    unittest.main()
