import unittest
from unittest.mock import Mock

from app.validation.error_messages import error_messages
from app.validation.validators import MonthYearCheck
from wtforms.validators import ValidationError


class TestMonthYearValidator(unittest.TestCase):
    def test_month_year_date_validator_none(self):
        validator = MonthYearCheck()

        mock_form = Mock()
        mock_form.month.data = None
        mock_form.year.data = None

        mock_field = Mock()

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages['INVALID_DATE'], str(ite.exception))

    def test_month_year_date_validator_empty_string(self):

        validator = MonthYearCheck()

        mock_form = Mock()
        mock_form.month.data = ""
        mock_form.year.data = ""

        mock_field = Mock()

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages['INVALID_DATE'], str(ite.exception))

    def test_month_year_date_validator_missing_month(self):
        validator = MonthYearCheck()

        mock_form = Mock()
        mock_form.month.data = ""
        mock_form.year.data = "2017"

        mock_field = Mock()

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages['INVALID_DATE'], str(ite.exception))

    def test_month_year_date_validator_missing_year(self):
        validator = MonthYearCheck()

        mock_form = Mock()
        mock_form.month.data = "12"
        mock_form.year.data = ""

        mock_field = Mock()

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages['INVALID_DATE'], str(ite.exception))

    def test_month_year_date_validator_invalid_month(self):
        validator = MonthYearCheck()

        mock_form = Mock()
        mock_form.month.data = "13"
        mock_form.year.data = "2017"

        mock_field = Mock()

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages['INVALID_DATE'], str(ite.exception))

    def test_month_year_date_validator_invalid_year(self):
        validator = MonthYearCheck()

        mock_form = Mock()
        mock_form.month.data = "12"
        mock_form.year.data = "17"

        mock_field = Mock()

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages['INVALID_DATE'], str(ite.exception))

    def test_month_year_date_validator_valid(self):
        validator = MonthYearCheck()

        mock_form = Mock()
        mock_form.month.data = "01"
        mock_form.year.data = "2017"

        mock_field = Mock()

        try:
            validator(mock_form, mock_field)
        except ValidationError:
            self.fail("Valid date raised ValidationError")
