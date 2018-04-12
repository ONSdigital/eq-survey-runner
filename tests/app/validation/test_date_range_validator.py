import unittest
from unittest.mock import Mock
from wtforms.validators import ValidationError

from app.validation.error_messages import error_messages
from app.validation.validators import DateRangeCheck


class TestDateRangeValidator(unittest.TestCase):
    """
    With each of the date range tests, on init the validator is passed
    the 'to' range data dictionary, whilst the validator receives the from
    form data as an object during the validation call
    """
    def test_date_range_matching_dates(self):

        validator = DateRangeCheck()

        period_from = Mock()
        period_from.data = {
            'day': '03',
            'month': '01',
            'year': '2016'
        }

        period_to = Mock()
        period_to.data = {
            'day': '03',
            'month': '01',
            'year': '2016'
        }
        mock_form = Mock()

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, period_from, period_to)

        self.assertEqual(error_messages['INVALID_DATE_RANGE'], str(ite.exception))

    def test_date_range_to_before_from(self):

        validator = DateRangeCheck()

        period_from = Mock()
        period_from.data = {
            'day': '20',
            'month': '01',
            'year': '2018'
        }

        period_to = Mock()
        period_to.data = {
            'day': '20',
            'month': '01',
            'year': '2016'
        }

        mock_form = Mock()

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, period_from, period_to)

        self.assertEqual(error_messages['INVALID_DATE_RANGE'], str(ite.exception))

    @staticmethod
    def test_date_range_valid():

        validator = DateRangeCheck()

        period_from = Mock()
        period_from.data = {
            'day': '01',
            'month': '01',
            'year': '2016'
        }

        period_to = Mock()
        period_to.data = {
            'day': '05',
            'month': '01',
            'year': '2017'
        }

        mock_form = Mock()
        validator(mock_form, period_from, period_to)

    @staticmethod
    def test_valid_month_year_date_range():

        validator = DateRangeCheck()

        period_from = Mock()
        period_from.data = {
            'month': '09',
            'year': '2016'
        }

        period_to = Mock()
        period_to.data = {
            'month': '01',
            'year': '2018'
        }

        mock_form = Mock()
        validator(mock_form, period_from, period_to)

    def test_invalid_month_year_date_range(self):

        validator = DateRangeCheck()

        period_from = Mock()
        period_from.data = {
            'month': '07',
            'year': '2018'
        }

        period_to = Mock()
        period_to.data = {
            'month': '06',
            'year': '2018'
        }

        mock_form = Mock()

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, period_from, period_to)

        self.assertEqual(error_messages['INVALID_DATE_RANGE'], str(ite.exception))
