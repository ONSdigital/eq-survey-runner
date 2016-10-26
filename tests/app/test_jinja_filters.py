from datetime import datetime
from unittest import TestCase

from app.jinja_filters import pretty_date
from app.jinja_filters import pretty_date_range


class TestJinjaFilters(TestCase):

    def test_format_pretty_date(self):
        # Given
        date = datetime.strptime('01/01/17', '%d/%m/%y')

        # When
        pretty_value = pretty_date(date)

        self.assertEquals(pretty_value, '1 January 2017')

    def test_format_pretty_date_range(self):
        # Given
        date_range = {'from': datetime.strptime('01/01/17', '%d/%m/%y'),
                      'to': datetime.strptime('01/01/18', '%d/%m/%y')}
        # When
        pretty_value = pretty_date_range(date_range)

        self.assertEquals(pretty_value, '01 Jan 2017 to 01 Jan 2018')
