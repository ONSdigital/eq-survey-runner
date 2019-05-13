import unittest
from unittest.mock import Mock, patch
from wtforms.validators import StopValidation, ValidationError

from app.validation.error_messages import error_messages
from app.validation.validators import NumberCheck, DecimalPlaces
from app.forms.fields import get_number_field, CustomDecimalField, MAX_DECIMAL_PLACES
from app.data_model.answer_store import AnswerStore


# pylint: disable=no-member
@patch('app.jinja_filters.flask_babel.get_locale', Mock(return_value='en_GB'))
class TestNumberValidator(unittest.TestCase):
    """
    Number validator uses the raw data from the input, which is in a list
    """

    def test_none_invalid(self):
        validator = NumberCheck()

        mock_form = Mock()
        mock_field = Mock()
        mock_field.raw_data = [None]

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages['INVALID_NUMBER'], str(ite.exception))

    def test_empty_string_invalid(self):
        validator = NumberCheck()

        mock_form = Mock()
        mock_field = Mock()
        mock_field.raw_data = ['']

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages['INVALID_NUMBER'], str(ite.exception))

    def test_non_numeric_string_invalid(self):
        validator = NumberCheck()

        mock_form = Mock()
        mock_field = Mock()
        mock_field.raw_data = ['a']

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages['INVALID_NUMBER'], str(ite.exception))

    def test_numeric_exponential_invalid(self):
        validator = NumberCheck()

        mock_form = Mock()
        mock_field = Mock()
        mock_field.raw_data = ['2E2']

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages['INVALID_NUMBER'], str(ite.exception))

    def test_decimal_number_invalid(self):
        validator = DecimalPlaces(2)

        mock_form = Mock()
        mock_field = Mock()
        mock_field.raw_data = ['1.234']

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, mock_field)

        error_message = error_messages['INVALID_DECIMAL'] % dict(max=2)
        self.assertEqual(error_message, str(ite.exception))

    def test_space_invalid(self):
        validator = NumberCheck()

        mock_form = Mock()
        mock_field = Mock()
        mock_field.raw_data = [' ']

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages['INVALID_NUMBER'], str(ite.exception))

    def test_zero_valid(self):
        validator = NumberCheck()

        mock_form = Mock()
        mock_field = Mock()
        mock_field.raw_data = ['0']

        try:
            validator(mock_form, mock_field)
        except StopValidation:
            self.fail('Valid number raised StopValidation')

    def test_positive_number_valid(self):
        validator = NumberCheck()

        mock_form = Mock()
        mock_field = Mock()
        mock_field.raw_data = ['10']

        try:
            validator(mock_form, mock_field)
        except StopValidation:
            self.fail('Valid number raised StopValidation')

    def test_negative_number_valid(self):
        validator = NumberCheck()

        mock_form = Mock()
        mock_field = Mock()
        mock_field.raw_data = ['-10']

        try:
            validator(mock_form, mock_field)
        except StopValidation:
            self.fail('Valid number raised StopValidation')

    def test_manual_decimal(self):
        answer = {
            'decimal_places': 2,
            'label': 'Range Test 10 to 20',
            'mandatory': False,
            'validation': {
                'messages': {
                    'INVALID_NUMBER': 'Please only enter whole numbers into the field.',
                    'INVALID_DECIMAL': 'Please enter a number to 2 decimal places.',
                }
            },
            'id': 'test-range',
            'type': 'Currency',
        }
        label = answer['label']
        returned_error_messages = answer['validation']['messages']

        decimal_field = get_number_field(
            answer, label, '', returned_error_messages, AnswerStore(), False
        )

        self.assertTrue(decimal_field.field_class == CustomDecimalField)

        for validator in decimal_field.kwargs['validators']:
            if isinstance(validator, DecimalPlaces):
                test_validator = validator

        mock_form = Mock()
        decimal_field.raw_data = ['1.234']

        with self.assertRaises(ValidationError) as ite:
            test_validator(mock_form, decimal_field)

            self.assertEqual(
                str(ite.exception), returned_error_messages['INVALID_DECIMAL']
            )

        try:
            decimal_field.raw_data = ['1.23']
            test_validator(mock_form, decimal_field)
        except ValidationError:
            self.fail('Valid decimal raised ValidationError')

    def test_manual_decimal_too_large(self):
        answer = {
            'decimal_places': 10,
            'label': 'Range Test 10 to 20',
            'mandatory': False,
            'validation': {
                'messages': {
                    'INVALID_NUMBER': 'Please only enter whole numbers into the field.',
                    'INVALID_DECIMAL': 'Please enter a number to 2 decimal places.',
                }
            },
            'id': 'test-range',
            'type': 'Currency',
        }
        label = answer['label']
        returned_error_messages = answer['validation']['messages']

        with self.assertRaises(Exception) as ite:
            get_number_field(
                answer, label, '', returned_error_messages, AnswerStore(), False
            )

            self.assertEqual(
                str(ite.exception),
                'decimal_places: 10 > system maximum: {} for answer id: test-range'.format(
                    MAX_DECIMAL_PLACES
                ),
            )
