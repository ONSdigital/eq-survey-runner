import unittest
from app.validation.month_year_date_type_check import MonthYearDateTypeCheck
from app.validation.abstract_validator import AbstractValidator


class DateMonthYearTest(unittest.TestCase):

    def test_month_year_date_validator_none(self):

        month_year_date_type = MonthYearDateTypeCheck()
        result = month_year_date_type.validate(None)
        self.assertFalse(result.is_valid)
        self.assertEquals(len(result.errors), 1)
        self.assertEquals(AbstractValidator.INVALID_DATE, result.errors[0])

    def test_month_year_date_validator_empty_string(self):

        month_year_date_type = MonthYearDateTypeCheck()
        result = month_year_date_type.validate('')
        self.assertFalse(result.is_valid)
        self.assertEquals(len(result.errors), 1)
        self.assertEquals(AbstractValidator.INVALID_DATE, result.errors[0])

    def test_month_year_date_validator_missing_month(self):

        month_year_date_type = MonthYearDateTypeCheck()
        result = month_year_date_type.validate('/2017')
        self.assertFalse(result.is_valid)
        self.assertEquals(len(result.errors), 1)
        self.assertEquals(AbstractValidator.INVALID_DATE, result.errors[0])

    def test_month_year_date_validator_missing_year(self):

        month_year_date_type = MonthYearDateTypeCheck()
        result = month_year_date_type.validate('12/')
        self.assertFalse(result.is_valid)
        self.assertEquals(len(result.errors), 1)
        self.assertEquals(AbstractValidator.INVALID_DATE, result.errors[0])

    def test_month_year_date_validator_invalid_month(self):

        month_year_date_type = MonthYearDateTypeCheck()
        result = month_year_date_type.validate('13/2017')
        self.assertFalse(result.is_valid)
        self.assertEquals(len(result.errors), 1)
        self.assertEquals(AbstractValidator.INVALID_DATE, result.errors[0])

    def test_month_year_date_validator_invalid_year(self):

        month_year_date_type = MonthYearDateTypeCheck()
        result = month_year_date_type.validate('12/17')
        self.assertFalse(result.is_valid)
        self.assertEquals(len(result.errors), 1)
        self.assertEquals(AbstractValidator.INVALID_DATE, result.errors[0])

    def test_month_year_date_validator_valid(self):

        month_year_date_type = MonthYearDateTypeCheck()
        result = month_year_date_type.validate('01/2017')
        self.assertTrue(result.is_valid)
        self.assertEquals(len(result.errors), 0)
