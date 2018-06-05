import unittest
from unittest.mock import Mock
from wtforms.validators import ValidationError

from app.validation.error_messages import error_messages
from app.validation.validators import MutuallyExclusive


class TestMutuallyExclusive(unittest.TestCase):

    def setUp(self):
        options = [
            {'label': 'Cheese', 'value': 'Cheese'},
            {'label': 'Ham', 'value': 'Ham'},
            {'label': 'Pineapple', 'value': 'Pineapple'},
            {'label': 'Tuna', 'value': 'Tuna'},
            {'label': 'Pepperoni', 'value': 'Pepperoni'},
            {'description': 'Choose any other topping', 'label': 'Other', 'value': 'Other',
             'child_answer_id': 'other-answer-mandatory'},
            {'label': 'No extra toppings', 'value': 'None'}
        ]
        self.validator = MutuallyExclusive(options)
        self.mock_form = Mock()
        self.mock_field = Mock()

    def test_mutually_exclusive_exception(self):
        self.mock_field.data = ['Cheese', 'Ham', 'Pineapple', 'None']

        with self.assertRaises(ValidationError) as ite:
            self.validator(self.mock_form, self.mock_field)

        self.assertEqual(error_messages['MUTUALLY_EXCLUSIVE'] % dict(non_exclusives='"Cheese", "Ham" and "Pineapple"', exclusive='No extra toppings'),
                         str(ite.exception))


    def test_mutually_exclusive_exception_single_non_exclusive(self):
        self.mock_field.data = ['Cheese', 'None']

        with self.assertRaises(ValidationError) as ite:
            self.validator(self.mock_form, self.mock_field)

        self.assertEqual(error_messages['MUTUALLY_EXCLUSIVE'] % dict(non_exclusives='"Cheese"', exclusive='No extra toppings'),
                         str(ite.exception))


    def test_mutually_exclusive_pass(self):
        # Non-Exclusive values only
        self.mock_field.data = ['Cheese', 'Ham', 'Pineapple', 'Tuna', 'Pepperoni', 'Other']
        self.validator(self.mock_form, self.mock_field)

        # Exclusive value only
        self.mock_field.data = ['None']
        self.validator(self.mock_form, self.mock_field)
