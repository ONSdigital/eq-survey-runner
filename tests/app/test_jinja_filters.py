# coding: utf-8

from datetime import datetime
from unittest import TestCase

from mock import Mock

from app.jinja_filters import format_date, format_conditional_date, format_currency, get_currency_symbol, \
     format_multilined_string, format_percentage, format_start_end_date, format_household_member_name, \
     format_str_as_date, format_str_as_date_range, format_str_as_month_year_date, format_number_to_alphabetic_letter, \
     format_unit, format_currency_for_input, format_number, format_list, format_household_member_name_possessive


class TestJinjaFilters(TestCase):  # pylint: disable=too-many-public-methods

    def test_format_currency_for_input(self):
        self.assertEqual(format_currency_for_input('100', 2), '100.00')
        self.assertEqual(format_currency_for_input('100.0', 2), '100.00')
        self.assertEqual(format_currency_for_input('100.00', 2), '100.00')
        self.assertEqual(format_currency_for_input('1000'), '1,000')
        self.assertEqual(format_currency_for_input('10000'), '10,000')
        self.assertEqual(format_currency_for_input('100000000'), '100,000,000')
        self.assertEqual(format_currency_for_input('100000000', 2), '100,000,000.00')
        self.assertEqual(format_currency_for_input(0, 2), '0.00')
        self.assertEqual(format_currency_for_input(0), '0')
        self.assertEqual(format_currency_for_input(''), '')
        self.assertEqual(format_currency_for_input(None), '')

    def test_get_currency_symbol(self):
        self.assertEqual(get_currency_symbol('GBP'), '£')
        self.assertEqual(get_currency_symbol('EUR'), '€')
        self.assertEqual(get_currency_symbol('USD'), 'US$')
        self.assertEqual(get_currency_symbol('JPY'), 'JP¥')
        self.assertEqual(get_currency_symbol(''), '')

    def test_format_currency(self):
        self.assertEqual(format_currency('11', 'GBP'), '£11.00')
        self.assertEqual(format_currency('11.99', 'GBP'), '£11.99')
        self.assertEqual(format_currency('11000', 'USD'), 'US$11,000.00')
        self.assertEqual(format_currency(0), '£0.00')
        self.assertEqual(format_currency('', ), '')
        self.assertEqual(format_currency(None), '')

    def test_format_number(self):
        self.assertEqual(format_number(123), '123')
        self.assertEqual(format_number('123.4'), '123.4')
        self.assertEqual(format_number('123.40'), '123.4')
        self.assertEqual(format_number('1000'), '1,000')
        self.assertEqual(format_number('10000'), '10,000')
        self.assertEqual(format_number('100000000'), '100,000,000')
        self.assertEqual(format_number(0), '0')
        self.assertEqual(format_number(''), '')
        self.assertEqual(format_number(None), '')

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

        self.assertEqual(format_value, "<span class='date'>1 January 2017</span>")

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
        self.assertIn('No valid dates passed to format_conditional_dates filter', str(exception.exception))

    def test_format_conditional_date(self):
        # Given

        datelist = [('12/01/2016', '12/02/2016', '12 January 2016'),
                    ('23/12/2017', None, '23 December 2017'),
                    (datetime(2019, 5, 12), None, '12 May 2019'),
                    (None, datetime(2017, 6, 22), '22 June 2017'),
                    ('12/08/2017', datetime(2017, 9, 10), '12 August 2017'),
                    (datetime(2018, 4, 7), '12/3/2018', '7 April 2018'),
                    (None, datetime(2017, 10, 12), '12 October 2017'),
                    (datetime(2019, 10, 12), datetime(2017, 9, 12), '12 October 2019')]

        # When
        for triple in datelist:
            date1 = triple[0]
            date2 = triple[1]
            #dates = (date1, date2)
            format_value = format_conditional_date(date1, date2)

            # Then
            self.assertEqual(format_value, "<span class='date'>{date}</span>".format(date=triple[2]))


    def test_format_start_end_date(self):
        # Given
        start_date = datetime.strptime('01/01/17', '%d/%m/%y')
        end_date = datetime.strptime('31/01/17', '%d/%m/%y')

        # When
        format_value = format_start_end_date(start_date, end_date)

        # Then
        self.assertEqual(format_value, "<span class='date'>1 January 2017</span> to <span class='date'>31 January 2017</span>")

    def test_format_start_end_date_missing_end_date(self):
        # Given
        start_date = datetime.strptime('01/01/17', '%d/%m/%y')

        # When
        format_value = format_start_end_date(start_date)

        # Then
        self.assertEqual(format_value, "<span class='date'>1 January 2017</span>")

    def test_format_str_as_date_range(self):
        # Given
        date_range = {'from': '01/01/2017',
                      'to': '01/01/2018'}
        # When
        format_value = format_str_as_date_range(date_range)

        self.assertEqual(format_value, "<span class='date'>1 January 2017</span> to <span class='date'>1 January 2018</span>")

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

        self.assertEqual(format_value, "<span class='date'>2 March 2017</span>")

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

    def test_format_household_member_name_possessive(self):
        # Given
        name = ['John', 'Doe']

        # When
        format_value = format_household_member_name_possessive(name)

        self.assertEqual(format_value, "John Doe's")

    def test_format_household_member_name_possessive_trailing_s(self):
        # Given
        name = ['John', 'Does']

        # When
        format_value = format_household_member_name_possessive(name)

        self.assertEqual(format_value, "John Does'")

    def test_format_percentage(self):
        self.assertEqual(format_percentage('100'), '100%')
        self.assertEqual(format_percentage(100), '100%')
        self.assertEqual(format_percentage(4.5), '4.5%')

    def test_format_number_to_alphabetic_letter(self):
        self.assertEqual(format_number_to_alphabetic_letter(0), 'a')
        self.assertEqual(format_number_to_alphabetic_letter(4), 'e')
        self.assertEqual(format_number_to_alphabetic_letter(25), 'z')
        self.assertEqual(format_number_to_alphabetic_letter(-1), '')

    def test_format_unit(self):
        self.assertEqual(format_unit('length-meter', 100), '100 m')
        self.assertEqual(format_unit('length-centimeter', 100), '100 cm')
        self.assertEqual(format_unit('length-mile', 100), '100 mi')
        self.assertEqual(format_unit('length-kilometer', 100), '100 km')
        self.assertEqual(format_unit('area-square-meter', 100), '100 m²')
        self.assertEqual(format_unit('area-square-centimeter', 100), '100 cm²')
        self.assertEqual(format_unit('area-square-kilometer', 100), '100 km²')
        self.assertEqual(format_unit('area-square-mile', 100), '100 sq mi')
        self.assertEqual(format_unit('area-hectare', 100), '100 ha')
        self.assertEqual(format_unit('area-acre', 100), '100 ac')
        self.assertEqual(format_unit('volume-cubic-meter', 100), '100 m³')
        self.assertEqual(format_unit('volume-cubic-centimeter', 100), '100 cm³')
        self.assertEqual(format_unit('volume-liter', 100), '100 l')
        self.assertEqual(format_unit('volume-hectoliter', 100), '100 hl')
        self.assertEqual(format_unit('volume-megaliter', 100), '100 Ml')

    def test_format_list(self):
        list_items = [['item 1', 'item 2']]

        formatted_value = format_list(list_items)

        expected_value = '<ul><li>item 1</li><li>item 2</li></ul>'

        self.assertEqual(expected_value, formatted_value)

    def test_format_list_with_no_input(self):
        list_items = []

        formatted_value = format_list(list_items)

        self.assertEqual('', formatted_value)

    def test_format_list_with_empty_list(self):
        list_items = [[]]

        formatted_value = format_list(list_items)

        self.assertEqual('', formatted_value)
