import unittest
from app.validation.date_range_check import DateRangeCheck
from app.validation.abstract_validator import AbstractValidator


class DateRangeTypeTest(unittest.TestCase):

    def test_date_range_type_validator(self):
        date_range_type = DateRangeCheck()

        # validate None
        result = date_range_type.validate(None)
        self.assertFalse(result.is_valid)
        self.assertEquals(len(result.errors), 1)
        self.assertEquals(AbstractValidator.INVALID_DATE, result.errors[0])

        # empty date
        result = date_range_type.validate('{}')
        self.assertFalse(result.is_valid)
        self.assertEquals(len(result.errors), 1)
        self.assertEquals(AbstractValidator.INVALID_DATE, result.errors[0])

        # invalid from date
        result = date_range_type.validate(['/01/2016', '01/01/2016'])
        self.assertFalse(result.is_valid)
        self.assertEquals(len(result.errors), 1)
        self.assertEquals(AbstractValidator.INVALID_DATE, result.errors[0])

        # invalid to date
        result = date_range_type.validate(['01/01/2016', '/01/2016'])
        self.assertFalse(result.is_valid)
        self.assertEquals(len(result.errors), 1)
        self.assertEquals(AbstractValidator.INVALID_DATE, result.errors[0])

        # just from date
        result = date_range_type.validate(['01/01/2017'])
        self.assertFalse(result.is_valid)

        # just to date
        result = date_range_type.validate(['01/01/2017'])
        self.assertFalse(result.is_valid)

        # dates the same
        result = date_range_type.validate(['01/01/2016', '01/01/2016'])
        self.assertFalse(result.is_valid)
        self.assertEquals(len(result.errors), 1)
        self.assertEquals(AbstractValidator.INVALID_DATE_RANGE_TO_FROM_SAME, result.errors[0])

        # from date before to date
        result = date_range_type.validate(['20/01/2018', '20/02/2016'])
        self.assertFalse(result.is_valid)
        self.assertEquals(len(result.errors), 1)
        self.assertEquals(AbstractValidator.INVALID_DATE_RANGE_TO_BEFORE_FROM, result.errors[0])

        # valid date range
        result = date_range_type.validate(['01/01/2016', '01/01/2017'])
        self.assertTrue(result.is_valid)
        self.assertEquals(len(result.errors), 0)

if __name__ == '__main__':
    unittest.main()
