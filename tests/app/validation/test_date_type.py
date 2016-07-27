import unittest
from app.validation.date_type_check import DateTypeCheck
from app.validation.abstract_validator import AbstractValidator


class DateTypeTest(unittest.TestCase):

    def test_date_type_validator(self):
        date_type = DateTypeCheck()

        # validate None
        result = date_type.validate(None)
        self.assertFalse(result.is_valid)
        self.assertEquals(len(result.errors), 1)
        self.assertEquals(AbstractValidator.INVALID_DATE, result.errors[0])

        # empty string
        result = date_type.validate('')
        self.assertFalse(result.is_valid)
        self.assertEquals(len(result.errors), 1)
        self.assertEquals(AbstractValidator.INVALID_DATE, result.errors[0])

        # missing day
        result = date_type.validate('2016/12/')
        self.assertFalse(result.is_valid)
        self.assertEquals(len(result.errors), 1)
        self.assertEquals(AbstractValidator.INVALID_DATE, result.errors[0])

        # missing month
        result = date_type.validate('2016//01')
        self.assertFalse(result.is_valid)
        self.assertEquals(len(result.errors), 1)
        self.assertEquals(AbstractValidator.INVALID_DATE, result.errors[0])

        # missing year
        result = date_type.validate('/12/01')
        self.assertFalse(result.is_valid)
        self.assertEquals(len(result.errors), 1)
        self.assertEquals(AbstractValidator.INVALID_DATE, result.errors[0])

        # invalid day
        result = date_type.validate('2016/12/40')
        self.assertFalse(result.is_valid)
        self.assertEquals(len(result.errors), 1)
        self.assertEquals(AbstractValidator.INVALID_DATE, result.errors[0])

        # invalid month
        result = date_type.validate('2016/13/01')
        self.assertFalse(result.is_valid)
        self.assertEquals(len(result.errors), 1)
        self.assertEquals(AbstractValidator.INVALID_DATE, result.errors[0])

        # invalid year
        result = date_type.validate('16/12/01')  # year should be 4 digits
        self.assertFalse(result.is_valid)
        self.assertEquals(len(result.errors), 1)
        self.assertEquals(AbstractValidator.INVALID_DATE, result.errors[0])

        # Leap year
        result = date_type.validate('2015/02/29')  # 2015 was not a leap year
        self.assertFalse(result.is_valid)
        self.assertEquals(len(result.errors), 1)
        self.assertEquals(AbstractValidator.INVALID_DATE, result.errors[0])

        result = date_type.validate('2016/02/29')  # 2016 WAS a leap year
        self.assertTrue(result.is_valid)
        self.assertEquals(len(result.errors), 0)

        # valid dates
        result = date_type.validate('2016/01/01')
        self.assertTrue(result.is_valid)
        self.assertEquals(len(result.errors), 0)

        result = date_type.validate('2016/12/1')
        self.assertTrue(result.is_valid)
        self.assertEquals(len(result.errors), 0)

        result = date_type.validate('2016/3/01')
        self.assertTrue(result.is_valid)
        self.assertEquals(len(result.errors), 0)


if __name__ == '__main__':
    unittest.main()
