from unittest import TestCase

from app.schema.answers.month_year_date_answer import MonthYearDateAnswer


class TestMonthYearDateAnswer(TestCase):

    def test_month_year_date_answer_non_mandatory(self):
        date_widget = MonthYearDateAnswer('1234')
        response = date_widget.get_user_input({'1234-month':'', '1234-year':''})
        self.assertIsNone(response)

    def test_month_year_date_answer_mandatory(self):
        date_widget = MonthYearDateAnswer('1234')
        response = date_widget.get_user_input({'1234-month':'1', '1234-year':'2017'})
        self.assertRegexpMatches(response, "1/2017")
