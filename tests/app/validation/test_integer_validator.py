import unittest
from unittest.mock import Mock

from app.validation.error_messages import error_messages
from app.validation.validators import IntegerCheck
from wtforms.validators import StopValidation


class TestIntegerValidator(unittest.TestCase):
    """
    Integer validator uses the raw data from the input, which is in a list
    """
    def test_none_invalid(self):
        validator = IntegerCheck()

        mock_form = Mock()
        mock_field = Mock()
        mock_field.raw_data = [None]

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages['NOT_INTEGER'], str(ite.exception))

    def test_empty_string_invalid(self):
        validator = IntegerCheck()

        mock_form = Mock()
        mock_field = Mock()
        mock_field.raw_data = ['']

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages['NOT_INTEGER'], str(ite.exception))

    def test_non_numeric_string_invalid(self):
        validator = IntegerCheck()

        mock_form = Mock()
        mock_field = Mock()
        mock_field.raw_data = ['a']

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages['NOT_INTEGER'], str(ite.exception))

    def test_decimal_number_invalid(self):
        validator = IntegerCheck()

        mock_form = Mock()
        mock_field = Mock()
        mock_field.raw_data = ['1.3']

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages['NOT_INTEGER'], str(ite.exception))

    def test_space_invalid(self):
        validator = IntegerCheck()

        mock_form = Mock()
        mock_field = Mock()
        mock_field.raw_data = [' ']

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages['NOT_INTEGER'], str(ite.exception))

    def test_zero_valid(self):
        validator = IntegerCheck()

        mock_form = Mock()
        mock_field = Mock()
        mock_field.raw_data = ['0']

        try:
            validator(mock_form, mock_field)
        except StopValidation:
            self.fail("Valid integer raised StopValidation")

    def test_positive_integer_valid(self):
        validator = IntegerCheck()

        mock_form = Mock()
        mock_field = Mock()
        mock_field.raw_data = ['10']

        try:
            validator(mock_form, mock_field)
        except StopValidation:
            self.fail("Valid integer raised StopValidation")

    def test_negative_integer_valid(self):
        validator = IntegerCheck()

        mock_form = Mock()
        mock_field = Mock()
        mock_field.raw_data = ['-10']

        try:
            validator(mock_form, mock_field)
        except StopValidation:
            self.fail("Valid integer raised StopValidation")
