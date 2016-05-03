import unittest
from app.authentication.user import User


class TestUser(unittest.TestCase):

    def test_get_user_id(self):
        user = User("1")
        self.assertEquals("1", user.get_user_id())


