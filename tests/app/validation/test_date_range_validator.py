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
        period_from.data = '2016-01-03'

        period_to = Mock()
        period_to.data = '2016-01-03'
        mock_form = Mock()

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, period_from, period_to)

        self.assertEqual(error_messages['INVALID_DATE_RANGE'], str(ite.exception))

    def test_date_range_to_before_from(self):

        validator = DateRangeCheck()

        period_from = Mock()
        period_from.data = '2018-01-20'

        period_to = Mock()
        period_to.data = '2016-01-20'

        mock_form = Mock()

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, period_from, period_to)

        self.assertEqual(error_messages['INVALID_DATE_RANGE'], str(ite.exception))

    @staticmethod
    def test_date_range_and_period_valid():

        period_min = {'days': 50}
        period_max = {'years': 1, 'months': 1, 'days': 5}
        validator = DateRangeCheck(period_min=period_min, period_max=period_max)

        period_from = Mock()
        period_from.data = '2016-01-01'

        period_to = Mock()
        period_to.data = '2017-01-05'

        mock_form = Mock()
        validator(mock_form, period_from, period_to)

    @staticmethod
    def test_valid_month_year_date_range():

        validator = DateRangeCheck()

        period_from = Mock()
        period_from.data = '2016-09'

        period_to = Mock()
        period_to.data = '2018-01'

        mock_form = Mock()
        validator(mock_form, period_from, period_to)

    def test_invalid_month_year_date_range(self):

        validator = DateRangeCheck()

        period_from = Mock()
        period_from.data = '2018-07'

        period_to = Mock()
        period_to.data = '2018-06'

        mock_form = Mock()

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, period_from, period_to)

        self.assertEqual(error_messages['INVALID_DATE_RANGE'], str(ite.exception))

    def test_date_range_with_too_small_period(self):

        period_min = {'days': 20}
        validator = DateRangeCheck(period_min=period_min)

        period_from = Mock()
        period_from.data = '2016-02-01'

        period_to = Mock()
        period_to.data = '2016-02-12'

        mock_form = Mock()

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, period_from, period_to)

        self.assertEqual(
            'Enter a reporting period greater than or equal to 20 days.',
            str(ite.exception),
        )

    def test_date_range_with_too_large_period(self):

        period_max = {'months': 1}
        validator = DateRangeCheck(period_max=period_max)

        period_from = Mock()
        period_from.data = '2016-02-11'

        period_to = Mock()
        period_to.data = '2016-03-14'

        mock_form = Mock()

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, period_from, period_to)

        self.assertEqual(
            'Enter a reporting period less than or equal to 1 month.',
            str(ite.exception),
        )

    def test_bespoke_message_playback(self):
        message = {'DATE_PERIOD_TOO_LARGE': 'Test %(max)s'}
        period_max = {'years': 2, 'months': 1, 'days': 3}
        validator = DateRangeCheck(messages=message, period_max=period_max)

        period_from = Mock()
        period_from.data = '2016-02-11'

        period_to = Mock()
        period_to.data = '2018-03-19'

        mock_form = Mock()

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, period_from, period_to)

        self.assertEqual('Test 2 years, 1 month, 3 days', str(ite.exception))

    def test_message_combinations(self):
        period_from = Mock()
        period_from.data = '2016-02-11'

        period_to = Mock()
        period_to.data = '2018-03-19'

        mock_form = Mock()

        # Max years, month, days
        period_max = {'years': 2, 'months': 1, 'days': 3}
        validator = DateRangeCheck(period_max=period_max)

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, period_from, period_to)

        self.assertEqual(
            'Enter a reporting period less than or equal to 2 years, 1 month, 3 days.',
            str(ite.exception),
        )

        # Max month, day
        period_max = {'months': 2, 'days': 1}
        validator = DateRangeCheck(period_max=period_max)

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, period_from, period_to)

        self.assertEqual(
            'Enter a reporting period less than or equal to 2 months, 1 day.',
            str(ite.exception),
        )

        # Max years, days
        period_min = {'years': 3, 'days': 2}
        validator = DateRangeCheck(period_min=period_min)

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, period_from, period_to)

        self.assertEqual(
            'Enter a reporting period greater than or equal to 3 years, 2 days.',
            str(ite.exception),
        )
