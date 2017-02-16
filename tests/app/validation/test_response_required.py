import unittest
from unittest.mock import Mock

from app.validation.validators import ResponseRequired
from wtforms.validators import StopValidation
from app.validation.error_messages import error_messages


class TestResponseRequiredValidator(unittest.TestCase):
    def test_response_empty_invalid(self):
        validator = ResponseRequired()

        mock_form = Mock()

        mock_field = Mock()
        mock_field.raw_data = ['']
        mock_field.errors = []

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages['MANDATORY'], str(ite.exception))

    def test_response_blank_invalid(self):
        validator = ResponseRequired()

        mock_form = Mock()

        mock_field = Mock()
        mock_field.raw_data = ['                           ']
        mock_field.errors = []

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages['MANDATORY'], str(ite.exception))

    def test_required_empty(self):

        validator = ResponseRequired()

        mock_form = Mock()

        mock_field = Mock()
        mock_field.raw_data = ['Here is some valid input']

        try:
            validator(mock_form, mock_field)
        except StopValidation:
            self.fail("Response that needs further validation raised StopValidation")

    def test_required_contains_content(self):

        validator = ResponseRequired()

        mock_form = Mock()

        mock_field = Mock()
        mock_field.raw_data = ['           Here is some valid input             ']

        try:
            validator(mock_form, mock_field)
        except StopValidation:
            self.fail("Response that needs further validation raised StopValidation")

    def test_response_blank_valid_when_whitespace_on(self):
        validator = ResponseRequired(strip_whitespace=False)

        mock_form = Mock()

        mock_field = Mock()
        mock_field.raw_data = ['                      ']
        mock_field.errors = []

        try:
            validator(mock_form, mock_field)
        except StopValidation:
            self.fail("Response that needs further validation raised StopValidation")
