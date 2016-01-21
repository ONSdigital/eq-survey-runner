import unittest
from app.authentication.jwt_decoder import NoTokenException, InvalidTokenException, decode_token


class NoTokenTest(unittest.TestCase):

    def test(self):
        no_token = NoTokenException("test")
        self.assertEquals(str(no_token), "test")


class UnauthorizedTest(unittest.TestCase):

    def test(self):
        unauthorized = InvalidTokenException("test")
        self.assertEquals(str(unauthorized), "test")


class JWTDecodeTest(unittest.TestCase):

    def test_decode(self):
        encrypted_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3O" \
                          "DkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ"
        token = decode_token(encrypted_token)
        self.assertEquals("John Doe", token.get("name"))

    def test_no_token(self):
        encrypted_token = None
        self.assertRaises(NoTokenException, decode_token, encrypted_token)

    def test_invalid_token(self):
        encrypted_token = "asdasdasdasd"
        self.assertRaises(InvalidTokenException, decode_token, encrypted_token)


if __name__ == '__main__':
    unittest.main()
