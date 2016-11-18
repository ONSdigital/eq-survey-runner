from app.schema.widgets.date_widget import DateWidget

from unittest import TestCase


class TestDateAnswer(TestCase):

    def test_date_answer_non_mandatory(self):
        date_widget = DateWidget('1234')
        response = date_widget.get_user_input({'1234-day': '', '1234-month':'', '1234-year':''})
        self.assertIsNone(response)

    def test_date_answer_mandatory(self):
        date_widget = DateWidget('1234')
        response = date_widget.get_user_input({'1234-day':'1', '1234-month':'2', '1234-year':'2017'})
        self.assertRegexpMatches(response, "1/2/2017")
