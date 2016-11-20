import unittest
# from app.schema.answer import Response
# from app.schema.question import Question
# from app.schema.section import Section
# from app.schema.block import Block
# from app.schema.questionnaire import Questionnaire
# from app.schema.group import Group
from app.validation.integer_type_check import IntegerTypeCheck
from app.validation.abstract_validator import AbstractValidator


class IntegerTest(unittest.TestCase):

    def test_integer_validator(self):
        integer = IntegerTypeCheck()

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
        self.assertTrue(result.is_valid)
        self.assertEquals(len(result.errors), 0)

        # <space>
        result = integer.validate(' ')
        self.assertFalse(result.is_valid)
        self.assertEquals(len(result.errors), 1)
        self.assertEquals(AbstractValidator.NOT_INTEGER, result.errors[0])

        # Too big
        result = integer.validate('10000000000')       # 11 digits
        self.assertFalse(result.is_valid)
        self.assertEquals(len(result.errors),  1)
        self.assertEquals(AbstractValidator.INTEGER_TOO_LARGE, result.errors[0])

        # Big enough
        result = integer.validate('9999999999')        # 10 digits
        self.assertTrue(result.is_valid)
        self.assertEquals(len(result.errors),  0)
        self.assertEquals(len(result.warnings),  0)


if __name__ == '__main__':
    unittest.main()
