import unittest
from datetime import datetime

from app.utilities.format_submitted_time import format_submitted_time


class TestFormattedSubmitTime(unittest.TestCase):

    def test_with_zero_ms(self):
        test_date = datetime.today().strftime('%Y-%m-%dT%H:%M:%S')
        test_date_zero_ms = test_date
        self.assertTrue(format_submitted_time(test_date_zero_ms) == datetime.strptime(test_date, '%Y-%m-%dT%H:%M:%S'))

    def test_with_ms(self):
        test_date = datetime.today().strftime('%Y-%m-%dT%H:%M:%S.%f')
        self.assertTrue(format_submitted_time(test_date) == datetime.strptime(test_date, '%Y-%m-%dT%H:%M:%S.%f'))


if __name__ == '__main__':
    unittest.main()
