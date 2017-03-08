import unittest
from unittest.mock import Mock

from app.validation.error_messages import error_messages
from app.validation.validators import NumberRange
from wtforms.validators import ValidationError


class TestNumberRangeValidator(unittest.TestCase):
    """
    Number range validator uses the data, which is already known as integer
    """
    def test_too_small_when_min_set_is_invalid(self):
        validator = NumberRange(minimum=0)

        mock_form = Mock()
        mock_field = Mock()
        mock_field.data = -10

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages['NEGATIVE_INTEGER'], str(ite.exception))

    def test_too_big_when_max_set_is_invalid(self):
        validator = NumberRange(maximum=9999999999)

        mock_form = Mock()
        mock_field = Mock()
        mock_field.data = 10000000000

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages['INTEGER_TOO_LARGE'], str(ite.exception))

    def test_within_range(self):
        validator = NumberRange(minimum=0, maximum=10)

        mock_form = Mock()
        mock_field = Mock()
        mock_field.data = 10

        try:
            validator(mock_form, mock_field)
        except ValidationError:
            self.fail("Valid integer raised ValidationError")

    def test_within_range_at_min(self):
        validator = NumberRange(minimum=0, maximum=9999999999)

        mock_form = Mock()
        mock_field = Mock()
        mock_field.data = 0

        try:
            validator(mock_form, mock_field)
        except ValidationError:
            self.fail("Valid integer raised ValidationError")

    def test_within_range_at_max(self):
        validator = NumberRange(minimum=0, maximum=9999999999)

        mock_form = Mock()
        mock_field = Mock()
        mock_field.data = 9999999999

        try:
            validator(mock_form, mock_field)
        except ValidationError:
            self.fail("Valid integer raised ValidationError")

