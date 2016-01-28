from app.authentication.no_token_exception import NoTokenException
import unittest


class NoTokenExceptionTest(unittest.TestCase):

    def test(self):
        no_token = NoTokenException("test")
        self.assertEquals("test", str(no_token))


if __name__ == '__main__':
    unittest.main()
