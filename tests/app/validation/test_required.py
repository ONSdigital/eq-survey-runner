from app.validation.mandatory_check import MandatoryCheck
import unittest


class RequiredTest(unittest.TestCase):

    def test_required_validator(self):
        required = MandatoryCheck()

        # validate None
        result = required.validate(None)
        self.assertFalse(result.is_valid)
        self.assertEquals(len(result.errors), 1)
        self.assertEquals('This field is mandatory', result.errors[0])

        # empty string
        result = required.validate('')
        self.assertFalse(result.is_valid)
        self.assertEquals(len(result.errors), 1)
        self.assertEquals('This field is mandatory', result.errors[0])

        # non-numeric string
        result = required.validate('a')
        self.assertTrue(result.is_valid)
        self.assertEquals(len(result.errors), 0)

        # 0
        result = required.validate('0')
        self.assertTrue(result.is_valid)
        self.assertEquals(len(result.errors), 0)

        # <space>
        result = required.validate(' ')
        self.assertFalse(result.is_valid)
        self.assertEquals(len(result.errors), 1)
        self.assertEquals('This field is mandatory', result.errors[0])
