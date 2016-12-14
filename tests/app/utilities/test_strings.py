from app.utilities import strings
import unittest


class TestStrings(unittest.TestCase):

    def test_to_bytes_with_string(self):
        b = strings.to_bytes('abc')
        self.assertEqual(b, b'abc')

    def test_to_bytes_with_bytes(self):
        b = strings.to_bytes(b'def')
        self.assertEqual(b, b'def')

    def test_to_bytes_with_none(self):
        b = strings.to_bytes(None)
        self.assertEqual(b, None)

    def test_to_string_with_string(self):
        s = strings.to_str('hij')
        self.assertEqual(s, 'hij')

    def test_to_string_with_bytes(self):
        s = strings.to_str(b'klm')
        self.assertEqual(s, 'klm')

    def test_to_string_with_None(self):
        s = strings.to_str(None)
        self.assertEqual(s, None)

if __name__ == '__main__':
    unittest.main()
