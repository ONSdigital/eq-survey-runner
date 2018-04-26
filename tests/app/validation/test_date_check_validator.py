import unittest
from unittest.mock import Mock
from wtforms.validators import StopValidation

from app.validation.error_messages import error_messages
from app.validation.validators import DateCheck


class TestDateCheckValidator(unittest.TestCase):
    def test_date_type_validator_none(self):
        validator = DateCheck()

        mock_form = Mock()
        mock_form.data = {
            'day': '',
            'month': '',
            'year': ''
        }

        mock_field = Mock()

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages['INVALID_DATE'], str(ite.exception))

    def test_date_type_validator_empty_string(self):
        validator = DateCheck()

        mock_form = Mock()
        mock_form.data = {
            'day': '',
            'month': '',
            'year': ''
        }

        mock_field = Mock()

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages['INVALID_DATE'], str(ite.exception))

    def test_date_type_validator_missing_day(self):
        validator = DateCheck()

        mock_form = Mock()
        mock_form.data = {
            'day': '',
            'month': '12',
            'year': '2016'
        }

        mock_field = Mock()

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages['INVALID_DATE'], str(ite.exception))

    def test_date_type_validator_missing_month(self):
        validator = DateCheck()

        mock_form = Mock()
        mock_form.data = {
            'day': '03',
            'month': '',
            'year': '2016'
        }

        mock_field = Mock()

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages['INVALID_DATE'], str(ite.exception))

    def test_date_type_validator_missing_year(self):
        validator = DateCheck()

        mock_form = Mock()
        mock_form.data = {
            'day': '03',
            'month': '12',
            'year': ''
        }

        mock_field = Mock()

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages['INVALID_DATE'], str(ite.exception))

    def test_date_type_validator_invalid_day(self):
        validator = DateCheck()

        mock_form = Mock()
        mock_form.data = {
            'day': '40',
            'month': '12',
            'year': '2016'
        }

        mock_field = Mock()

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages['INVALID_DATE'], str(ite.exception))

    def test_date_type_validator_invalid_month(self):
        validator = DateCheck()

        mock_form = Mock()
        mock_form.data = {
            'day': '20',
            'month': '13',
            'year': '2016'
        }

        mock_field = Mock()

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages['INVALID_DATE'], str(ite.exception))

    def test_date_type_validator_invalid_year(self):
        validator = DateCheck()

        mock_form = Mock()
        mock_form.data = {
            'day': '20',
            'month': '12',
            'year': '16'
        }

        mock_field = Mock()

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages['INVALID_DATE'], str(ite.exception))

    def test_date_type_validator_invalid_leap_year(self):

        validator = DateCheck()

        # 2015 was not a leap year
        mock_form = Mock()
        mock_form.data = {
            'day': '29',
            'month': '02',
            'year': '2015'
        }

        mock_field = Mock()

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages['INVALID_DATE'], str(ite.exception))

    @staticmethod
    def test_date_type_validator_valid_leap_year():
        validator = DateCheck()

        # 2016 WAS a leap year
        mock_form = Mock()
        mock_form.data = {
            'day': '29',
            'month': '02',
            'year': '2016'
        }

        mock_field = Mock()
        validator(mock_form, mock_field)

    @staticmethod
    def test_date_type_validator_valid_dates():
        validator = DateCheck()

        mock_form = Mock()
        mock_form.data = {
            'day': '29',
            'month': '01',
            'year': '2016'
        }

        mock_field = Mock()
        validator(mock_form, mock_field)

        mock_form = Mock()
        mock_form.data = {
            'day': '01',
            'month': '12',
            'year': '2016'
        }

        mock_field = Mock()
        validator(mock_form, mock_field)

        mock_form = Mock()
        mock_form.data = {
            'day': '03',
            'month': '03',
            'year': '2016'
        }

        mock_field = Mock()
        validator(mock_form, mock_field)
