import unittest
from unittest.mock import Mock

from app.validation.error_messages import error_messages
from app.validation.validators import DateCheck
from wtforms.validators import StopValidation


class TestDateCheckValidator(unittest.TestCase):
    def test_date_type_validator_none(self):
        validator = DateCheck()

        mock_form = Mock()
        mock_form.day.data = None
        mock_form.month.data = None
        mock_form.year.data = None

        mock_field = Mock()

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages['INVALID_DATE'], str(ite.exception))

    def test_date_type_validator_empty_string(self):
        validator = DateCheck()

        mock_form = Mock()
        mock_form.day.data = ''
        mock_form.month.data = ''
        mock_form.year.data = ''

        mock_field = Mock()

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages['INVALID_DATE'], str(ite.exception))

    def test_date_type_validator_missing_day(self):
        validator = DateCheck()

        mock_form = Mock()
        mock_form.day.data = ''
        mock_form.month.data = '12'
        mock_form.year.data = '2016'

        mock_field = Mock()

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages['INVALID_DATE'], str(ite.exception))

    def test_date_type_validator_missing_month(self):
        validator = DateCheck()

        mock_form = Mock()
        mock_form.day.data = '01'
        mock_form.month.data = ''
        mock_form.year.data = '2016'

        mock_field = Mock()

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages['INVALID_DATE'], str(ite.exception))

    def test_date_type_validator_missing_year(self):
        validator = DateCheck()

        mock_form = Mock()
        mock_form.day.data = '01'
        mock_form.month.data = '12'
        mock_form.year.data = ''

        mock_field = Mock()

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages['INVALID_DATE'], str(ite.exception))

    def test_date_type_validator_invalid_day(self):
        validator = DateCheck()

        mock_form = Mock()
        mock_form.day.data = '40'
        mock_form.month.data = '12'
        mock_form.year.data = '2016'

        mock_field = Mock()

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages['INVALID_DATE'], str(ite.exception))

    def test_date_type_validator_invalid_month(self):
        validator = DateCheck()

        mock_form = Mock()
        mock_form.day.data = '01'
        mock_form.month.data = '13'
        mock_form.year.data = '2016'

        mock_field = Mock()

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages['INVALID_DATE'], str(ite.exception))

    def test_date_type_validator_invalid_year(self):
        validator = DateCheck()

        mock_form = Mock()
        mock_form.day.data = '01'
        mock_form.month.data = '1'
        mock_form.year.data = '16'

        mock_field = Mock()

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages['INVALID_DATE'], str(ite.exception))

    def test_date_type_validator_invalid_leap_year(self):

        validator = DateCheck()

        # 2015 was not a leap year
        mock_form = Mock()
        mock_form.day.data = '29'
        mock_form.month.data = '02'
        mock_form.year.data = '2015'

        mock_field = Mock()

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages['INVALID_DATE'], str(ite.exception))

    def test_date_type_validator_valid_leap_year(self):
        validator = DateCheck()

        # 2016 WAS a leap year
        mock_form = Mock()
        mock_form.day.data = '29'
        mock_form.month.data = "02"
        mock_form.year.data = "2016"

        mock_field = Mock()

        try:
            validator(mock_form, mock_field)
        except StopValidation:
            self.fail("Valid date raised StopValidation")

    def test_date_type_validator_valid_dates(self):

        validator = DateCheck()

        mock_form = Mock()
        mock_form.day.data = '01'
        mock_form.month.data = "01"
        mock_form.year.data = "2016"

        mock_field = Mock()

        try:
            validator(mock_form, mock_field)
        except StopValidation:
            self.fail("Valid date raised StopValidation")

        mock_form = Mock()
        mock_form.day.data = '1'
        mock_form.month.data = "12"
        mock_form.year.data = "2016"

        mock_field = Mock()

        try:
            validator(mock_form, mock_field)
        except StopValidation:
            self.fail("Valid date raised StopValidation")

        mock_form = Mock()
        mock_form.day.data = '01'
        mock_form.month.data = "03"
        mock_form.year.data = "2016"

        mock_field = Mock()

        try:
            validator(mock_form, mock_field)
        except StopValidation:
            self.fail("Valid date raised StopValidation")
