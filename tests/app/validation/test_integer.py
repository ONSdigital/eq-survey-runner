import unittest
from app.model.response import Response
from app.model.question import Question
from app.model.section import Section
from app.model.block import Block
from app.model.questionnaire import Questionnaire
from app.model.group import Group
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


if __name__ == '__main__':
    unittest.main()
