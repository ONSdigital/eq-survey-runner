from unittest import TestCase

from app.schema.answers.month_year_date_answer import MonthYearDateAnswer

from app.schema.exceptions import TypeCheckingException


class TestMonthYearDateAnswer(TestCase):

    def test_month_year_date_answer(self):
        month_year_date_answer = MonthYearDateAnswer('1234')
        post_data = {'1234': '1/2000'}
        result = month_year_date_answer.get_typed_value(post_data)
        self.assertEquals(result, '1/2000')

    def test_month_year_date_answer_incomplete_date(self):
        month_year_date_answer = MonthYearDateAnswer('1234')
        post_data = {'1234': '1/'}
        self.assertRaises(TypeCheckingException, month_year_date_answer.get_typed_value, post_data)

    def test_month_year_date_answer_text_empty(self):
        month_year_date_answer = MonthYearDateAnswer('1234')
        post_data = {}
        self.assertRaises(TypeCheckingException, month_year_date_answer.get_typed_value, post_data)

    def test_month_year_date_answer_non_dict(self):
        month_year_date_answer = MonthYearDateAnswer('1234')
        post_data = '1/2000'
        result = month_year_date_answer.get_typed_value(post_data)
        self.assertEquals(result, '1/2000')
