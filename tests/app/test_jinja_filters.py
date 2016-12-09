from datetime import datetime
from unittest import TestCase

from app.jinja_filters import format_date
from app.jinja_filters import format_str_as_date_range
from app.jinja_filters import format_str_as_date
from app.jinja_filters import format_str_as_month_year_date
from app.jinja_filters import format_household_member_name


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

    def test_format_household_member_name(self):
        # Given
        name = ['John', 'Doe']

        # When
        format_value = format_household_member_name(name)

        self.assertEqual(format_value, 'John Doe')

    def test_format_household_member_name_no_surname(self):
        # Given
        name = ['John', '']

        # When
        format_value = format_household_member_name(name)

        self.assertEqual(format_value, 'John')

    def test_format_household_member_name_surname_is_none(self):
        # Given
        name = ['John', None]

        # When
        format_value = format_household_member_name(name)

        self.assertEqual(format_value, 'John')

    def test_format_household_member_name_no_first_name(self):
        # Given
        name = ['', 'Doe']

        # When
        format_value = format_household_member_name(name)

        self.assertEqual(format_value, 'Doe')

    def test_format_household_member_name_first_name_is_none(self):
        # Given
        name = [None, 'Doe']

        # When
        format_value = format_household_member_name(name)

        self.assertEqual(format_value, 'Doe')

    def test_format_household_member_name_first_middle_and_last(self):
        # Given
        name = ['John', 'J', 'Doe']

        # When
        format_value = format_household_member_name(name)

        self.assertEqual(format_value, 'John J Doe')

    def test_format_household_member_name_no_middle_name(self):
        # Given
        name = ['John', '', 'Doe']

        # When
        format_value = format_household_member_name(name)

        self.assertEqual(format_value, 'John Doe')

    def test_format_household_member_name_middle_name_is_none(self):
        # Given
        name = ['John', None, 'Doe']

        # When
        format_value = format_household_member_name(name)

        self.assertEqual(format_value, 'John Doe')

    def test_format_household_member_name_trim_spaces(self):
        # Given
        name = ['John  ', '   Doe   ']

        # When
        format_value = format_household_member_name(name)

        self.assertEqual(format_value, 'John Doe')
