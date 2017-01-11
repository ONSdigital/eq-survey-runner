import unittest

from app.validation.abstract_validator import AbstractValidator
from app.validation.textarea_type_check import TextAreaTypeCheck


class TextAreaTest(unittest.TestCase):

    def test_textarea_validator(self):
        textarea = TextAreaTypeCheck()

        # validate integer
        result = textarea.validate(1)
        self.assertFalse(result.is_valid)
        self.assertEqual(len(result.errors), 1)
        self.assertEqual(AbstractValidator.NOT_STRING, result.errors[0])

        # validate None
        result = textarea.validate(None)
        self.assertFalse(result.is_valid)
        self.assertEqual(len(result.errors), 1)
        self.assertEqual(AbstractValidator.NOT_STRING, result.errors[0])

        # validate <space>
        result = textarea.validate(' ')
        self.assertFalse(result.is_valid)

        # validate string
        result = textarea.validate('string')
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors),  0)
        self.assertEqual(len(result.warnings),  0)

if __name__ == '__main__':
    unittest.main()
