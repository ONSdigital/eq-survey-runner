from unittest import TestCase

from app.schema.answers.percentage_answer import PercentageAnswer


class TestPercentageAnswer(TestCase):

    def test_percentage_answer_valid(self):
        percentage_answer = PercentageAnswer('percent')
        post_data = '75'
        result = percentage_answer.get_typed_value(post_data)
        self.assertEquals(result, 75.0)

    def test_percentage_answer_not_number(self):
        percentage_answer = PercentageAnswer('percent')
        post_data = {'percent': 'abc'}
        self.assertRaises(ValueError, percentage_answer.get_typed_value, post_data)

    def test_percentage_answer_empty(self):
        percentage_answer = PercentageAnswer('percent')
        post_data = {}
        self.assertRaises(ValueError, percentage_answer.get_typed_value, post_data)
