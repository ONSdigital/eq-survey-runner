import unittest
from unittest.mock import Mock, patch

from wtforms.validators import ValidationError

from app.validation.error_messages import error_messages
from app.validation.validators import SumCheck, format_playback_value


@patch('app.jinja_filters.flask_babel.get_locale', Mock(return_value='en_GB'))
class TestSumCheckValidator(unittest.TestCase):
    """
    Sum check validator evaluates a calculated total against a target total, given a condition
    """

    def test_equal_condition_check(self):
        validator = SumCheck()

        mock_form = Mock()

        conditions = ['equals']
        calculation_total = 10
        target_total = 11.5

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, conditions, calculation_total, target_total)

        self.assertEqual(
            error_messages['TOTAL_SUM_NOT_EQUALS']
            % dict(total=format_playback_value(target_total)),
            str(ite.exception),
        )

    def test_less_or_equal_condition_check(self):
        validator = SumCheck()

        mock_form = Mock()

        conditions = ['less than', 'equals']
        calculation_total = 20
        target_total = 11.5

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, conditions, calculation_total, target_total)

        self.assertEqual(
            error_messages['TOTAL_SUM_NOT_LESS_THAN_OR_EQUALS']
            % dict(total=format_playback_value(target_total)),
            str(ite.exception),
        )

    def test_less_than_condition_check(self):
        validator = SumCheck()

        mock_form = Mock()

        conditions = ['less than']
        calculation_total = 11.99
        target_total = 11.5

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, conditions, calculation_total, target_total)

        self.assertEqual(
            error_messages['TOTAL_SUM_NOT_LESS_THAN']
            % dict(total=format_playback_value(target_total)),
            str(ite.exception),
        )

    def test_greater_than_condition_check(self):
        validator = SumCheck()

        mock_form = Mock()

        conditions = ['greater than']
        calculation_total = 11.99
        target_total = 12.5

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, conditions, calculation_total, target_total)

        self.assertEqual(
            error_messages['TOTAL_SUM_NOT_GREATER_THAN']
            % dict(total=format_playback_value(target_total)),
            str(ite.exception),
        )

    def test_greater_or_equal_condition_check(self):
        validator = SumCheck()

        mock_form = Mock()

        conditions = ['greater than', 'equals']
        calculation_total = 11.99
        target_total = 12.5

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, conditions, calculation_total, target_total)

        self.assertEqual(
            error_messages['TOTAL_SUM_NOT_GREATER_THAN_OR_EQUALS']
            % dict(total=format_playback_value(target_total)),
            str(ite.exception),
        )

    def test_currency_playback(self):
        validator = SumCheck(currency='EUR')

        mock_form = Mock()

        conditions = ['equals']
        calculation_total = 10
        target_total = 11.5

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, conditions, calculation_total, target_total)

        self.assertEqual(
            error_messages['TOTAL_SUM_NOT_EQUALS']
            % dict(total=format_playback_value(target_total, currency='EUR')),
            str(ite.exception),
        )

    def test_bespoke_message_playback(self):
        message = {'TOTAL_SUM_NOT_EQUALS': 'Test %(total)s'}
        validator = SumCheck(messages=message)

        mock_form = Mock()

        conditions = ['equals']
        calculation_total = 10
        target_total = 11.5

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, conditions, calculation_total, target_total)

        self.assertEqual('Test {}'.format(target_total), str(ite.exception))

    def test_valid_multiple_conditions(self):
        validator = SumCheck()

        mock_form = Mock()

        conditions = ['less than', 'equals']
        calculation_total = 13
        target_total = 11.5

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, conditions, calculation_total, target_total)

        self.assertEqual(
            error_messages['TOTAL_SUM_NOT_LESS_THAN_OR_EQUALS']
            % dict(total=format_playback_value(target_total)),
            str(ite.exception),
        )

    def test_invalid_multiple_conditions(self):
        validator = SumCheck()

        mock_form = Mock()

        conditions = ['less than', 'greater than']
        calculation_total = 10
        target_total = 11.5

        with self.assertRaises(Exception) as ite:
            validator(mock_form, conditions, calculation_total, target_total)

        self.assertEqual(
            'There are multiple conditions, but equals is not one of them. We only support <= and >=',
            str(ite.exception),
        )
