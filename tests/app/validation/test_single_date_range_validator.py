from unittest.mock import Mock
from wtforms.validators import ValidationError

from app.questionnaire.rules import convert_to_datetime
from app.validation.error_messages import error_messages
from app.validation.validators import SingleDatePeriodCheck
from tests.app.app_context_test_case import AppContextTestCase


class TestDateRangeValidator(AppContextTestCase):
    def test_invalid_single_date_period_minimum_date(self):
        minimum_date = convert_to_datetime('2016-03-31')
        validator = SingleDatePeriodCheck(minimum_date=minimum_date)

        mock_form = Mock()
        mock_form.data = '2016-01-29'

        mock_field = Mock()

        with self.app_request_context('/'):
            with self.assertRaises(ValidationError) as ite:
                validator(mock_form, mock_field)

            self.assertEqual(
                error_messages['SINGLE_DATE_PERIOD_TOO_EARLY']
                % dict(min='30 March 2016'),
                str(ite.exception),
            )

    def test_invalid_single_date_period_maximum_date(self):
        maximum_date = convert_to_datetime('2016-03-31')
        validator = SingleDatePeriodCheck(maximum_date=maximum_date)

        mock_form = Mock()
        mock_form.data = '2016-04-29'

        mock_field = Mock()

        with self.app_request_context('/'):
            with self.assertRaises(ValidationError) as ite:
                validator(mock_form, mock_field)

            self.assertEqual(
                error_messages['SINGLE_DATE_PERIOD_TOO_LATE']
                % dict(max='1 April 2016'),
                str(ite.exception),
            )

    def test_invalid_single_date_period_with_bespoke_message(self):
        maximum_date = convert_to_datetime('2016-03-31')
        message = {'SINGLE_DATE_PERIOD_TOO_LATE': 'Test %(max)s'}
        validator = SingleDatePeriodCheck(messages=message, maximum_date=maximum_date)

        mock_form = Mock()
        mock_form.data = '2016-04-29'

        mock_field = Mock()

        with self.app_request_context('/'):
            with self.assertRaises(ValidationError) as ite:
                validator(mock_form, mock_field)

            self.assertEqual('Test 1 April 2016', str(ite.exception))

    @staticmethod
    def test_valid_single_date_period():
        minimum_date = convert_to_datetime('2016-03-20')
        maximum_date = convert_to_datetime('2016-03-31')
        validator = SingleDatePeriodCheck(
            minimum_date=minimum_date, maximum_date=maximum_date
        )

        mock_form = Mock()
        mock_form.data = '2016-03-26'

        mock_field = Mock()

        validator(mock_form, mock_field)
