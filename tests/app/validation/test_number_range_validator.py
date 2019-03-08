import unittest
from unittest.mock import Mock, patch
from wtforms.validators import ValidationError

from app.jinja_filters import format_number
from app.validation.error_messages import error_messages
from app.validation.validators import NumberRange
from app.forms.fields import get_number_field, CustomIntegerField
from app.data_model.answer_store import Answer, AnswerStore


# pylint: disable=no-member
@patch('app.jinja_filters.flask_babel.get_locale', Mock(return_value='en_GB'))
class TestNumberRangeValidator(unittest.TestCase):
    """
    Number range validator uses the data, which is already known as integer
    """

    def setUp(self):
        self.store = AnswerStore()

        answer1 = Answer(
            answer_id='set-minimum',
            value=10,
        )
        answer2 = Answer(
            answer_id='set-maximum',
            value=20,
        )
        answer3 = Answer(
            answer_id='set-maximum-cat',
            value='cat',
        )

        self.store.add_or_update(answer1)
        self.store.add_or_update(answer2)
        self.store.add_or_update(answer3)

    def tearDown(self):
        self.store.clear()

    def test_too_small_when_min_set_is_invalid(self):
        validator = NumberRange(minimum=0)

        mock_form = Mock()
        mock_field = Mock()
        mock_field.data = -10

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages['NUMBER_TOO_SMALL'] % dict(min=0), str(ite.exception))

    def test_too_big_when_max_set_is_invalid(self):
        validator = NumberRange(maximum=9999999999)

        mock_form = Mock()
        mock_field = Mock()
        mock_field.data = 10000000000

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages['NUMBER_TOO_LARGE'] % dict(max=format_number(9999999999)), str(ite.exception))

    def test_within_range(self):
        validator = NumberRange(minimum=0, maximum=10)

        mock_form = Mock()
        mock_field = Mock()
        mock_field.data = 10

        try:
            validator(mock_form, mock_field)
        except ValidationError:
            self.fail('Valid integer raised ValidationError')

    def test_within_range_at_min(self):
        validator = NumberRange(minimum=0, maximum=9999999999)

        mock_form = Mock()
        mock_field = Mock()
        mock_field.data = 0

        try:
            validator(mock_form, mock_field)
        except ValidationError:
            self.fail('Valid integer raised ValidationError')

    def test_within_range_at_max(self):
        validator = NumberRange(minimum=0, maximum=9999999999)

        mock_form = Mock()
        mock_field = Mock()
        mock_field.data = 9999999999

        try:
            validator(mock_form, mock_field)
        except ValidationError:
            self.fail('Valid integer raised ValidationError')

    def test_manual_min(self):
        answer = {
            'min_value': {
                'value': 10
            },
            'label': 'Min Test',
            'mandatory': False,
            'validation':
            {
                'messages': {
                    'INVALID_NUMBER': 'Please only enter whole numbers into the field.',
                    'NUMBER_TOO_SMALL': 'The minimum value allowed is 10. Please correct your answer.'
                }
            },
            'id': 'test-range',
            'type': 'Currency'
        }
        label = answer['label']
        returned_error_messages = answer['validation']['messages']

        integer_field = get_number_field(answer, label, '', returned_error_messages, self.store, False)

        self.assertTrue(integer_field.field_class == CustomIntegerField)

        for validator in integer_field.kwargs['validators']:
            if isinstance(validator, NumberRange):
                test_validator = validator

        mock_form = Mock()
        integer_field.data = 9

        with self.assertRaises(ValidationError) as ite:
            test_validator(mock_form, integer_field)

        self.assertEqual(str(ite.exception), returned_error_messages['NUMBER_TOO_SMALL'])

        try:
            integer_field.data = 10
            test_validator(mock_form, integer_field)
        except ValidationError:
            self.fail('Valid integer raised ValidationError')

    def test_manual_max(self):
        answer = {
            'max_value': {
                'value': 20
            },
            'label': 'Max Test',
            'mandatory': False,
            'validation':
                {
                    'messages': {
                        'INVALID_NUMBER': 'Please only enter whole numbers into the field.',
                        'NUMBER_TOO_LARGE': 'The maximum value allowed is 20. Please correct your answer.'
                    }
                },
            'id': 'test-range',
            'type': 'Currency'
        }
        label = answer['label']
        returned_error_messages = answer['validation']['messages']

        integer_field = get_number_field(answer, label, '', returned_error_messages, self.store, False)

        self.assertTrue(integer_field.field_class == CustomIntegerField)

        for validator in integer_field.kwargs['validators']:
            if isinstance(validator, NumberRange):
                test_validator = validator

        mock_form = Mock()
        integer_field.data = 21

        with self.assertRaises(ValidationError) as ite:
            test_validator(mock_form, integer_field)

        self.assertEqual(str(ite.exception), returned_error_messages['NUMBER_TOO_LARGE'])

        try:
            integer_field.data = 20
            test_validator(mock_form, integer_field)
        except ValidationError:
            self.fail('Valid integer raised ValidationError')

    def test_zero_max(self):
        max_value = 0
        answer = {
            'max_value': {
                'value': max_value
            },
            'label': 'Max Test',
            'mandatory': False,
            'id': 'test-range',
            'type': 'Currency'
        }
        label = answer['label']
        error_message = error_messages['NUMBER_TOO_LARGE'] % dict(max=max_value)

        integer_field = get_number_field(answer, label, '', error_messages, self.store, False)

        self.assertTrue(integer_field.field_class == CustomIntegerField)

        for validator in integer_field.kwargs['validators']:
            if isinstance(validator, NumberRange):
                test_validator = validator

        mock_form = Mock()
        integer_field.data = 1

        with self.assertRaises(ValidationError) as ite:
            test_validator(mock_form, integer_field)

        self.assertEqual(str(ite.exception), error_message)

        try:
            integer_field.data = 0
            test_validator(mock_form, integer_field)
        except ValidationError:
            self.fail('Valid integer raised ValidationError')

    def test_zero_min(self):
        min_value = 0
        answer = {
            'min_value': {
                'value': min_value
            },
            'label': 'Min Test',
            'mandatory': False,
            'id': 'test-range',
            'type': 'Currency'
        }
        label = answer['label']
        error_message = error_messages['NUMBER_TOO_SMALL'] % dict(min=min_value)

        integer_field = get_number_field(answer, label, '', error_messages, self.store, False)

        self.assertTrue(integer_field.field_class == CustomIntegerField)

        for validator in integer_field.kwargs['validators']:
            if isinstance(validator, NumberRange):
                test_validator = validator

        mock_form = Mock()
        integer_field.data = -1

        with self.assertRaises(ValidationError) as ite:
            test_validator(mock_form, integer_field)

        self.assertEqual(str(ite.exception), error_message)

        try:
            integer_field.data = 0
            test_validator(mock_form, integer_field)
        except ValidationError:
            self.fail('Valid integer raised ValidationError')

    def test_value_range(self):
        answer = {
            'min_value': {
                'value': 10
            },
            'max_value': {
                'value': 20
            },
            'label': 'Range Test 10 to 20',
            'mandatory': False,
            'validation': {
                'messages': {
                    'INVALID_NUMBER': 'Please only enter whole numbers into the field.',
                    'NUMBER_TOO_SMALL': 'The minimum value allowed is 10. Please correct your answer.',
                    'NUMBER_TOO_LARGE': 'The maximum value allowed is 20. Please correct your answer.'
                }
            },
            'id': 'test-range',
            'type': 'Currency'
        }
        label = answer['label']
        returned_error_messages = answer['validation']['messages']

        integer_field = get_number_field(answer, label, '', error_messages, self.store, False)

        self.assertTrue(integer_field.field_class == CustomIntegerField)

        for validator in integer_field.kwargs['validators']:
            if isinstance(validator, NumberRange):
                test_validator = validator

        mock_form = Mock()
        integer_field.data = 9

        with self.assertRaises(ValidationError) as ite:
            test_validator(mock_form, integer_field)

        self.assertEqual(str(ite.exception), returned_error_messages['NUMBER_TOO_SMALL'])

        try:
            integer_field.data = 20
            test_validator(mock_form, integer_field)
            integer_field.data = 10
            test_validator(mock_form, integer_field)
        except ValidationError:
            self.fail('Valid integer raised ValidationError')

    def test_answer_id_range(self):

        answer = {
            'min_value': {
                'answer_id': 'set-minimum'
            },
            'max_value': {
                'answer_id': 'set-maximum'
            },
            'label': 'Range Test 10 to 20',
            'mandatory': False,
            'validation': {
                'messages': {
                    'INVALID_NUMBER': 'Please only enter whole numbers into the field.',
                    'NUMBER_TOO_SMALL': 'The minimum value allowed is 10. Please correct your answer.',
                    'NUMBER_TOO_LARGE': 'The maximum value allowed is 20. Please correct your answer.'
                }
            },
            'id': 'test-range',
            'type': 'Currency'
        }
        label = answer['label']
        returned_error_messages = answer['validation']['messages']

        integer_field = get_number_field(answer, label, '', returned_error_messages, self.store, False)

        self.assertTrue(integer_field.field_class == CustomIntegerField)

        for validator in integer_field.kwargs['validators']:
            if isinstance(validator, NumberRange):
                test_validator = validator

        mock_form = Mock()
        integer_field.data = 9

        with self.assertRaises(ValidationError) as ite:
            test_validator(mock_form, integer_field)

        self.assertEqual(str(ite.exception), returned_error_messages['NUMBER_TOO_SMALL'])

        try:
            integer_field.data = 20
            test_validator(mock_form, integer_field)
            integer_field.data = 10
            test_validator(mock_form, integer_field)
        except ValidationError:
            self.fail('Valid integer raised ValidationError')

    def test_default_range(self):
        answer = {
            'decimal_places': 2,
            'label': 'Range Test 10 to 20',
            'mandatory': False,
            'validation': {
                'messages': {
                    'INVALID_NUMBER': 'Please only enter whole numbers into the field.',
                    'NUMBER_TOO_SMALL': 'The minimum value allowed is 10. Please correct your answer.',
                    'NUMBER_TOO_LARGE': 'The maximum value allowed is 20. Please correct your answer.'
                }
            },
            'id': 'test-range',
            'type': 'Currency'
        }
        label = answer['label']
        returned_error_messages = answer['validation']['messages']

        integer_field = get_number_field(answer, label, '', returned_error_messages, self.store, False)

        for validator in integer_field.kwargs['validators']:
            if isinstance(validator, NumberRange):
                test_validator = validator

        self.assertEqual(test_validator.maximum, 9999999999)
        self.assertEqual(test_validator.minimum, 0)

    def test_min_less_than_system_limits(self):
        answer = {
            'min_value': {
                'value': -1000000000
            },
            'id': 'test-range',
            'label': 'Range Test 10 to 20',
            'mandatory': False,
            'validation':
                {
                    'messages': {
                        'INVALID_NUMBER': 'Please only enter whole numbers into the field.',
                        'NUMBER_TOO_SMALL': 'The minimum value allowed is 10. Please correct your answer.',
                        'NUMBER_TOO_LARGE': 'The maximum value allowed is 20. Please correct your answer.'
                    }
                },
            'type': 'Currency'
        }
        label = answer['label']
        returned_error_messages = answer['validation']['messages']

        with self.assertRaises(Exception) as ite:
            get_number_field(answer, label, '', returned_error_messages, self.store, False)

        self.assertEqual(str(ite.exception),
                         'min_value: -1000000000 < system minimum: -999999999 for answer id: test-range')

    def test_max_greater_than_system_limits(self):
        answer = {
            'max_value': {
                'value': 10000000000
            },
            'id': 'test-range',
            'label': 'Range Test 10 to 20',
            'mandatory': False,
            'validation':
                {
                    'messages': {
                        'INVALID_NUMBER': 'Please only enter whole numbers into the field.',
                        'NUMBER_TOO_SMALL': 'The minimum value allowed is 10. Please correct your answer.',
                        'NUMBER_TOO_LARGE': 'The maximum value allowed is 20. Please correct your answer.'
                    }
                },
            'type': 'Currency'
        }
        label = answer['label']
        returned_error_messages = answer['validation']['messages']

        with self.assertRaises(Exception) as ite:
            get_number_field(answer, label, '', returned_error_messages, self.store, False)

        self.assertEqual(str(ite.exception),
                         'max_value: 10000000000 > system maximum: 9999999999 for answer id: test-range')

    def test_min_greater_than_max(self):
        answer = {
            'min_value': {
                'value': 20
            },
            'max_value': {
                'value': 10
            },
            'id': 'test-range',
            'label': 'Range Test 10 to 20',
            'mandatory': False,
            'validation':
                {
                    'messages': {
                        'INVALID_NUMBER': 'Please only enter whole numbers into the field.',
                        'NUMBER_TOO_SMALL': 'The minimum value allowed is 10. Please correct your answer.',
                        'NUMBER_TOO_LARGE': 'The maximum value allowed is 20. Please correct your answer.'
                    }
                },
            'type': 'Currency'
        }
        label = answer['label']
        returned_error_messages = answer['validation']['messages']

        with self.assertRaises(Exception) as ite:
            get_number_field(answer, label, '', returned_error_messages, self.store, False)

        self.assertEqual(str(ite.exception), 'min_value: 20 > max_value: 10 for answer id: test-range')

    def test_answer_id_invalid_type(self):

        answer = {
            'max_value': {
                'answer_id': 'set-maximum-cat'
            },
            'label': 'Range Test 10 to 20',
            'mandatory': False,
            'validation':
                {
                    'messages': {
                        'INVALID_NUMBER': 'Please only enter whole numbers into the field.',
                        'NUMBER_TOO_SMALL': 'The minimum value allowed is 10. Please correct your answer.',
                        'NUMBER_TOO_LARGE': 'The maximum value allowed is 20. Please correct your answer.'
                    }
                },
            'id': 'test-range',
            'type': 'Currency'
        }
        label = answer['label']
        returned_error_messages = answer['validation']['messages']

        with self.assertRaises(Exception) as ite:
            get_number_field(answer, label, '', returned_error_messages, self.store, False)

        self.assertEqual(str(ite.exception),
                         'answer: set-maximum-cat value: cat for answer id: test-range is not a valid number')

    def test_manual_min_exclusive(self):
        answer = {
            'min_value': {
                'value': 10,
                'exclusive': True
            },
            'label': 'Min Test',
            'mandatory': False,
            'validation':
                {
                    'messages': {
                        'INVALID_NUMBER': 'Please only enter whole numbers into the field.',
                        'NUMBER_TOO_SMALL_EXCLUSIVE': 'The minimum value allowed is 10. Please correct your answer.'
                    }
                },
            'id': 'test-range',
            'type': 'Currency'
        }
        label = answer['label']
        returned_error_messages = answer['validation']['messages']

        integer_field = get_number_field(answer, label, '', error_messages, self.store, False)

        self.assertTrue(integer_field.field_class == CustomIntegerField)

        for validator in integer_field.kwargs['validators']:
            if isinstance(validator, NumberRange):
                test_validator = validator

        mock_form = Mock()
        integer_field.data = 10

        with self.assertRaises(ValidationError) as ite:
            test_validator(mock_form, integer_field)

        self.assertEqual(str(ite.exception), returned_error_messages['NUMBER_TOO_SMALL_EXCLUSIVE'])

        try:
            integer_field.data = 11
            test_validator(mock_form, integer_field)
        except ValidationError:
            self.fail('Valid integer raised ValidationError')

    def test_manual_max_exclusive(self):
        answer = {
            'max_value': {
                'value': 20,
                'exclusive': True
            },
            'label': 'Max Test',
            'mandatory': False,
            'validation':
                {
                    'messages': {
                        'INVALID_NUMBER': 'Please only enter whole numbers into the field.',
                        'NUMBER_TOO_LARGE_EXCLUSIVE': 'The maximum value allowed is 20. Please correct your answer.'
                    }
                },
            'id': 'test-range',
            'type': 'Currency'
        }
        label = answer['label']
        returned_error_messages = answer['validation']['messages']

        integer_field = get_number_field(answer, label, '', returned_error_messages, self.store, False)

        self.assertTrue(integer_field.field_class == CustomIntegerField)

        for validator in integer_field.kwargs['validators']:
            if isinstance(validator, NumberRange):
                test_validator = validator

        mock_form = Mock()
        integer_field.data = 20

        with self.assertRaises(ValidationError) as ite:
            test_validator(mock_form, integer_field)

        self.assertEqual(str(ite.exception), returned_error_messages['NUMBER_TOO_LARGE_EXCLUSIVE'])

        try:
            integer_field.data = 19
            test_validator(mock_form, integer_field)
        except ValidationError:
            self.fail('Valid integer raised ValidationError')
