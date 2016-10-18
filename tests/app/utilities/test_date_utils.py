import unittest
import datetime

from app.utilities.date_utils import to_date


class TestDateUtils(unittest.TestCase):

    def test_parse_valid_date(self):
        date_strings = ("2016-04-01", "2016-09-09")

        for date_str in date_strings:
            parsed_date = to_date(date_str)

            self.assertTrue(isinstance(parsed_date, datetime.date))

    def test_parse_invalid_date(self):
        date_strings = ("2016-Mar-03", "a-random-string")

        for date_str in date_strings:
            parsed_date = to_date(date_str)

            self.assertEquals(parsed_date, None)

    def test_custom_date_string(self):
        custom_format = "%y-%b-%d"
        date_strings = ("16-Mar-03", "16-Aug-13")

        for date_str in date_strings:
            parsed_date = to_date(date_str, custom_format)

            self.assertTrue(isinstance(parsed_date, datetime.date))

    def test_parse_empty_date(self):
        date_str = None

        parsed_date = to_date(date_str)

        self.assertEquals(parsed_date, None)
