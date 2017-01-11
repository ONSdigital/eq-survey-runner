import datetime
import unittest

from app.utilities.date_utils import to_date


class TestDateUtils(unittest.TestCase):

    def test_parse_valid_date(self):
        self.assertTrue(isinstance(to_date("2016-04-01"), datetime.date))
        self.assertTrue(isinstance(to_date("2016-09-09"), datetime.date))

    def test_parse_invalid_date(self):
        self.assertEqual(to_date("2016-Mar-03"), None)
        self.assertEqual(to_date("a-random-string"), None)

    def test_custom_date_string(self):
        custom_format = "%y-%b-%d"

        parsed_date_1 = to_date("16-Mar-03", custom_format)
        parsed_date_2 = to_date("16-Aug-13", custom_format)

        self.assertTrue(isinstance(parsed_date_1, datetime.date))
        self.assertTrue(isinstance(parsed_date_2, datetime.date))

    def test_parse_empty_date(self):
        date_str = None

        parsed_date = to_date(date_str)

        self.assertEqual(parsed_date, None)
