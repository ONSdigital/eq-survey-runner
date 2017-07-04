from datetime import datetime
from unittest import TestCase

from mock import Mock

from app.jinja_filters import format_date, format_conditional_date, format_currency, format_multilined_string, \
     format_percentage, format_start_end_date
from app.jinja_filters import format_household_member_name
from app.jinja_filters import format_str_as_date
from app.jinja_filters import format_str_as_date_range
from app.jinja_filters import format_str_as_month_year_date
from app.jinja_filters import format_number_to_alphabetic_letter


class TestJinjaFilters(TestCase):  # pylint: disable=too-many-public-methods

    def test_format_currency(self):
        # Given
        currency = 1.12

        # When
        format_value = format_currency(currency)

        self.assertEqual(format_value, '£1.12')

    def test_format_currency_no_value_returns_empty_string(self):
        # Given
        currency = ''

        # When
        format_value = format_currency(currency)

        self.assertEqual(format_value, '')

    def test_format_multilined_string_matches_carriage_return(self):
        # Given
        new_line = 'this is on a new\rline'
        context = Mock()
        context.autoescape = False

        # When
        format_value = format_multilined_string(context, new_line)

        self.assertEqual(format_value, '<p>this is on a new<br>line</p>')

    def test_format_multilined_string_matches_new_line(self):
        # Given
        new_line = 'this is on a new\nline'
        context = Mock()
        context.autoescape = False

        # When
        format_value = format_multilined_string(context, new_line)

        self.assertEqual(format_value, '<p>this is on a new<br>line</p>')

    def test_format_multilined_string_matches_carriage_return_new_line(self):
        # Given
        new_line = 'this is on a new\r\nline'
        context = Mock()
        context.autoescape = False

        # When
        format_value = format_multilined_string(context, new_line)

        self.assertEqual(format_value, '<p>this is on a new<br>line</p>')

    def test_format_multilined_string(self):
        # Given
        new_line = 'this is\ron a\nnew\r\nline'
        context = Mock()
        context.autoescape = False

        # When
        format_value = format_multilined_string(context, new_line)

        self.assertEqual(format_value, '<p>this is<br>on a<br>new<br>line</p>')

    def test_format_multilined_string_auto_escape(self):
        # Given
        new_line = '<'
        context = Mock()
        context.autoescape = True

        # When
        format_value = format_multilined_string(context, new_line)

        self.assertEqual(str(format_value), '<p>&lt;</p>')

    def test_format_date(self):
        # Given
        date = datetime.strptime('01/01/17', '%d/%m/%y')

        # When
        format_value = format_date(date)

        self.assertEqual(format_value, '1 January 2017')

    def test_format_conditional_date_not_date(self):
        # Given       no test for integers this check was removed from jinja_filters

        invalid_input = [('1', None),
                         ('1/1/1', None)]

        # When
        for nonsense in invalid_input:
            date1 = nonsense[0]
            date2 = nonsense[1]
            with self.assertRaises(Exception) as exception:
                format_conditional_date(date1, date2)
        # Then
            self.assertIn("does not match format '%d/%m/%Y'", str(exception.exception))

    def test_format_conditional_date_not_set(self):
        # Given

        # When
        with self.assertRaises(Exception) as exception:
            format_conditional_date(None, None)

        # Then
        self.assertIn("No valid dates passed to format_conditional_dates filter", str(exception.exception))

    def test_format_conditional_date(self):
        # Given

        datelist = [('12/01/2016', '12/02/2016', '12 January 2016'),
                    ('23/12/2017', None, '23 December 2017'),
                    (datetime(2019, 5, 12), None, '12 May 2019'),
                    (None, datetime(2017, 6, 22), '22 June 2017'),
                    ('12/08/2017', datetime(2017, 9, 10), '12 August 2017'),
                    (datetime(2018, 4, 7), "12/3/2018", '7 April 2018'),
                    (None, datetime(2017, 10, 12), '12 October 2017'),
                    (datetime(2019, 10, 12), datetime(2017, 9, 12), '12 October 2019')]

        # When
        for triple in datelist:
            date1 = triple[0]
            date2 = triple[1]
            #dates = (date1, date2)
            format_value = format_conditional_date(date1, date2)

            # Then
            self.assertEqual(format_value, triple[2])

    def test_format_start_end_date(self):
        # Given
        start_date = datetime.strptime('01/01/17', '%d/%m/%y')
        end_date = datetime.strptime('31/01/17', '%d/%m/%y')

        # When
        format_value = format_start_end_date(start_date, end_date)

        # Then
        self.assertEqual(format_value, '1 January 2017 to 31 January 2017')

    def test_format_start_end_date_missing_end_date(self):
        # Given
        start_date = datetime.strptime('01/01/17', '%d/%m/%y')

        # When
        format_value = format_start_end_date(start_date)

        # Then
        self.assertEqual(format_value, '1 January 2017')

    def test_format_str_as_date_range(self):
        # Given
        date_range = {'from': '01/01/2017',
                      'to': '01/01/2018'}
        # When
        format_value = format_str_as_date_range(date_range)

        self.assertEqual(format_value, '01 January 2017 to 01 January 2018')

    def test_format_str_as_month_year_date(self):
        # Given
        month_year_date = '3/2018'

        # When
        format_value = format_str_as_month_year_date(month_year_date)

        self.assertEqual(format_value, 'March 2018')

    def test_format_str_as_date(self):
        # Given
        date = '02/03/2017'

        # When
        format_value = format_str_as_date(date)

        self.assertEqual(format_value, '02 March 2017')

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

    def test_format_percentage(self):
        self.assertEqual(format_percentage('100'), '100%')
        self.assertEqual(format_percentage(100), '100%')
        self.assertEqual(format_percentage(4.5), '4.5%')

    def test_format_number_to_alphabetic_letter(self):
        self.assertEqual(format_number_to_alphabetic_letter(0), 'a')
        self.assertEqual(format_number_to_alphabetic_letter(4), 'e')
        self.assertEqual(format_number_to_alphabetic_letter(25), 'z')
        self.assertEqual(format_number_to_alphabetic_letter(-1), '')
