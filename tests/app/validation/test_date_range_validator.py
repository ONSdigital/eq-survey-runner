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
        period_from.day.data = '01'
        period_from.month.data = '01'
        period_from.year.data = '2016'

        period_to = Mock()
        period_to.day.data = '01'
        period_to.month.data = '01'
        period_to.year.data = '2016'

        mock_form = Mock()

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, period_from, period_to)

        self.assertEqual(error_messages['INVALID_DATE_RANGE'], str(ite.exception))

    def test_date_range_to_before_from(self):

        validator = DateRangeCheck()

        period_from = Mock()
        period_from.day.data = '20'
        period_from.month.data = '01'
        period_from.year.data = '2018'

        period_to = Mock()
        period_to.day.data = '20'
        period_to.month.data = '01'
        period_to.year.data = '2016'

        mock_form = Mock()

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, period_from, period_to)

        self.assertEqual(error_messages['INVALID_DATE_RANGE'], str(ite.exception))

    def test_date_range_valid(self):

        validator = DateRangeCheck()

        period_from = Mock()
        period_from.day.data = '01'
        period_from.month.data = '01'
        period_from.year.data = '2016'

        period_to = Mock()
        period_to.day.data = '01'
        period_to.month.data = '01'
        period_to.year.data = '2017'

        mock_form = Mock()

        try:
            validator(mock_form, period_from, period_to)
        except ValidationError:
            self.fail('Valid date raised ValidationError')
