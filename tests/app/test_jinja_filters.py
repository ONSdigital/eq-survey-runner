from datetime import datetime
from unittest import TestCase

from app.jinja_filters import format_date
from app.jinja_filters import format_str_as_date_range
from app.jinja_filters import format_str_as_date
from app.jinja_filters import format_str_as_month_year_date


class TestJinjaFilters(TestCase):

    def test_format_date(self):
        # Given
        date = datetime.strptime('01/01/17', '%d/%m/%y')

        # When
        format_value = format_date(date)

        self.assertEquals(format_value, '1 January 2017')

    def test_format_str_as_date_range(self):
        # Given
        date_range = {'from': '01/01/2017',
                      'to': '01/01/2018'}
        # When
        format_value = format_str_as_date_range(date_range)

        self.assertEquals(format_value, '01 January 2017 to 01 January 2018')

    def test_format_str_as_month_year_date(self):
        # Given
        month_year_date = '3/2018'

        # When
        format_value = format_str_as_month_year_date(month_year_date)

        self.assertEquals(format_value, 'March 2018')

    def test_format_str_as_date(self):
        # Given
        date = '02/03/2017'

        # When
        format_value = format_str_as_date(date)

        self.assertEquals(format_value, '02 March 2017')
