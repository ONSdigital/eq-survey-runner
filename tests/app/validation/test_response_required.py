import unittest
from unittest.mock import Mock
from wtforms.validators import StopValidation

from app.validation.validators import ResponseRequired


class TestResponseRequiredValidator(unittest.TestCase):
    def test_response_empty_invalid(self):
        message = 'test_response_empty_invalid'
        validator = ResponseRequired(message)

        mock_form = Mock()

        mock_field = Mock()
        mock_field.raw_data = ['']
        mock_field.errors = []

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(message, str(ite.exception))

    def test_response_blank_invalid(self):
        message = 'test_response_blank_invalid'
        validator = ResponseRequired(message)

        mock_form = Mock()

        mock_field = Mock()
        mock_field.raw_data = ['                           ']
        mock_field.errors = []

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(message, str(ite.exception))

    def test_required_empty(self):

        message = 'test_required_empty'
        validator = ResponseRequired(message)

        mock_form = Mock()

        mock_field = Mock()
        mock_field.raw_data = ['Here is some valid input']

        try:
            validator(mock_form, mock_field)
        except StopValidation:
            self.fail('Response that needs further validation raised StopValidation')

    def test_required_contains_content(self):

        message = 'test_required_contains_content'
        validator = ResponseRequired(message)

        mock_form = Mock()

        mock_field = Mock()
        mock_field.raw_data = ['           Here is some valid input             ']

        try:
            validator(mock_form, mock_field)
        except StopValidation:
            self.fail('Response that needs further validation raised StopValidation')

    def test_response_blank_valid_when_whitespace_on(self):
        message = 'test_response_blank_valid_when_whitespace_on'
        validator = ResponseRequired(message=message, strip_whitespace=False)

        mock_form = Mock()

        mock_field = Mock()
        mock_field.raw_data = ['                      ']
        mock_field.errors = []

        try:
            validator(mock_form, mock_field)
        except StopValidation:
            self.fail('Response that needs further validation raised StopValidation')
