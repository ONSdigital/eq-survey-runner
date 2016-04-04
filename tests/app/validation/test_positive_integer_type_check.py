import unittest
from app.validation.positive_integer_type_check import PositiveIntegerTypeCheck
from app.validation.abstract_validator import AbstractValidator


class PositiveIntegerTest(unittest.TestCase):

    def test_positive_integer_type_check(self):
        integer = PositiveIntegerTypeCheck()

        # validate None
        result = integer.validate(None)
        self.assertFalse(result.is_valid)
        self.assertEquals(len(result.errors), 1)
        self.assertEquals(AbstractValidator.NOT_INTEGER, result.errors[0])

        # empty string
        result = integer.validate('')
        self.assertFalse(result.is_valid)
        self.assertEquals(len(result.errors), 1)
        self.assertEquals(AbstractValidator.NOT_INTEGER, result.errors[0])

        # non-numeric string
        result = integer.validate('a')
        self.assertFalse(result.is_valid)
        self.assertEquals(len(result.errors), 1)
        self.assertEquals(AbstractValidator.NOT_INTEGER, result.errors[0])

        # decimal number
        result = integer.validate('1.3')
        self.assertFalse(result.is_valid)
        self.assertEquals(len(result.errors), 1)
        self.assertEquals(AbstractValidator.NOT_INTEGER, result.errors[0])

        # 0
        result = integer.validate('0')
        self.assertTrue(result.is_valid)
        self.assertEquals(len(result.errors), 0)

        # positive integer
        result = integer.validate('10')
        self.assertTrue(result.is_valid)
        self.assertEquals(len(result.errors), 0)

        # negative integer
        result = integer.validate('-10')
        self.assertFalse(result.is_valid)
        self.assertEquals(len(result.errors), 1)
        self.assertEquals(AbstractValidator.NEGATIVE_INTEGER, result.errors[0])

        # <space>
        result = integer.validate(' ')
        self.assertFalse(result.is_valid)
        self.assertEquals(len(result.errors), 1)
        self.assertEquals(AbstractValidator.NOT_INTEGER, result.errors[0])


if __name__ == '__main__':
    unittest.main()
