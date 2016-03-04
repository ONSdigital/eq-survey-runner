import unittest
from app.validation.required import Required


class RequiredTest(unittest.TestCase):

    def test_required(self):
        q_data = "{}"
        validation_result = Required(q_data).validate()
        self.assertEquals(True, validation_result.is_valid())

if __name__ == '__main__':
    unittest.main()
