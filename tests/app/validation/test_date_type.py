import unittest

from app.validation.abstract_validator import AbstractValidator
from app.validation.date_type_check import DateTypeCheck


class DateTypeTest(unittest.TestCase):

    def test_date_type_validator(self):
        date_type = DateTypeCheck()

        # validate None
        result = date_type.validate(None)
        self.assertFalse(result.is_valid)
        self.assertEqual(len(result.errors), 1)
        self.assertEqual(AbstractValidator.INVALID_DATE, result.errors[0])

        # empty string
        result = date_type.validate('')
        self.assertFalse(result.is_valid)
        self.assertEqual(len(result.errors), 1)
        self.assertEqual(AbstractValidator.INVALID_DATE, result.errors[0])

        # missing day
        result = date_type.validate('/12/2016')
        self.assertFalse(result.is_valid)
        self.assertEqual(len(result.errors), 1)
        self.assertEqual(AbstractValidator.INVALID_DATE, result.errors[0])

        # missing month
        result = date_type.validate('01//2016')
        self.assertFalse(result.is_valid)
        self.assertEqual(len(result.errors), 1)
        self.assertEqual(AbstractValidator.INVALID_DATE, result.errors[0])

        # missing year
        result = date_type.validate('01/12/')
        self.assertFalse(result.is_valid)
        self.assertEqual(len(result.errors), 1)
        self.assertEqual(AbstractValidator.INVALID_DATE, result.errors[0])

        # invalid day
        result = date_type.validate('40/12/2016')
        self.assertFalse(result.is_valid)
        self.assertEqual(len(result.errors), 1)
        self.assertEqual(AbstractValidator.INVALID_DATE, result.errors[0])

        # invalid month
        result = date_type.validate('01/13/2016')
        self.assertFalse(result.is_valid)
        self.assertEqual(len(result.errors), 1)
        self.assertEqual(AbstractValidator.INVALID_DATE, result.errors[0])

        # invalid year
        result = date_type.validate('01/12/16')  # year should be 4 digits
        self.assertFalse(result.is_valid)
        self.assertEqual(len(result.errors), 1)
        self.assertEqual(AbstractValidator.INVALID_DATE, result.errors[0])

        # Leap year
        result = date_type.validate('29/02/2015')  # 2015 was not a leap year
        self.assertFalse(result.is_valid)
        self.assertEqual(len(result.errors), 1)
        self.assertEqual(AbstractValidator.INVALID_DATE, result.errors[0])

        result = date_type.validate('29/02/2016')  # 2016 WAS a leap year
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)

        # valid dates
        result = date_type.validate('01/01/2016')
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)

        result = date_type.validate('1/12/2016')
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)

        result = date_type.validate('01/3/2016')
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)


if __name__ == '__main__':
    unittest.main()
