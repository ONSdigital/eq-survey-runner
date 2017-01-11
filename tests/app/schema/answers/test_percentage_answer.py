from unittest import TestCase

from app.schema.answers.percentage_answer import PercentageAnswer
from app.schema.exceptions import TypeCheckingException


class TestPercentageAnswer(TestCase):

    def test_percentage_answer_valid(self):
        percentage_answer = PercentageAnswer('percent')
        post_data = '75'
        result = percentage_answer.get_typed_value(post_data)
        self.assertEqual(result, 75.0)

    def test_percentage_answer_not_number(self):
        percentage_answer = PercentageAnswer('percent')
        post_data = {'percent': 'abc'}
        self.assertRaises(TypeCheckingException, percentage_answer.get_typed_value, post_data)

    def test_percentage_answer_empty(self):
        percentage_answer = PercentageAnswer('percent')
        post_data = {}
        self.assertRaises(TypeCheckingException, percentage_answer.get_typed_value, post_data)

    def test_percentage_less_than_zero_should_error(self):
        percentage_answer = PercentageAnswer('percent')
        post_data = '-1'
        self.assertRaises(TypeCheckingException, percentage_answer.get_typed_value, post_data)

    def test_percentage_greater_than_hundred_should_error(self):
        percentage_answer = PercentageAnswer('percent')
        post_data = '101'
        self.assertRaises(TypeCheckingException, percentage_answer.get_typed_value, post_data)

    def test_percentage_non_integer_value_should_error(self):
        percentage_answer = PercentageAnswer('percent')
        post_data = '1.1'
        self.assertRaises(TypeCheckingException, percentage_answer.get_typed_value, post_data)
