import unittest
from app.validation.integer import Integer


class IntegerTest(unittest.TestCase):

    def test_integer(self):
        q_data = "{}"
        validation_result = Integer(q_data).validate()
        self.assertEquals(True, validation_result.is_valid())

if __name__ == '__main__':
    unittest.main()
