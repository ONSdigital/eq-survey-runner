from app.authentication.invalid_token_exception import InvalidTokenException
import unittest


class InvalidTokenExceptionTest(unittest.TestCase):

    def test(self):
        invalid_token = InvalidTokenException("test")
        self.assertEquals("test", str(invalid_token))

if __name__ == '__main__':
    unittest.main()

