# coding: utf-8
from datetime import datetime, timedelta
from types import SimpleNamespace
from unittest.mock import patch

from dateutil.relativedelta import relativedelta
from jinja2 import Undefined, Markup
from mock import Mock

from app.jinja_filters import (
    format_date, format_conditional_date, format_currency, get_currency_symbol,
    format_multilined_string, format_percentage, format_date_range,
    format_household_name, format_datetime,
    format_number_to_alphabetic_letter, format_unit,
    format_number, format_unordered_list, format_unordered_list_missing_items,
    format_unit_input_label, format_household_name_possessive, format_household_summary,
    concatenated_list, calculate_years_difference, get_current_date, as_london_tz,
    max_value, min_value, get_answer_label,
    format_duration, calculate_offset_from_weekday_in_last_whole_week, format_date_custom,
    format_date_range_no_repeated_month_year, format_repeating_summary, format_address_list, first_non_empty_item)
from tests.app.app_context_test_case import AppContextTestCase


class TestJinjaFilters(AppContextTestCase):  # pylint: disable=too-many-public-methods
    def setUp(self):
        self.autoescape_context = Mock(autoescape=True)
        super(TestJinjaFilters, self).setUp()

    @patch('app.jinja_filters.flask_babel.get_locale', Mock(return_value='en_GB'))
    def test_get_currency_symbol(self):
        self.assertEqual(get_currency_symbol('GBP'), '£')
        self.assertEqual(get_currency_symbol('EUR'), '€')
        self.assertEqual(get_currency_symbol('USD'), 'US$')
        self.assertEqual(get_currency_symbol('JPY'), 'JP¥')
        self.assertEqual(get_currency_symbol(''), '')

    @patch('app.jinja_filters.flask_babel.get_locale', Mock(return_value='en_GB'))
    def test_format_currency(self):
        self.assertEqual(format_currency(self.autoescape_context, '11', 'GBP'), "<span class='date'>£11.00</span>")
        self.assertEqual(format_currency(self.autoescape_context, '11.99', 'GBP'), "<span class='date'>£11.99</span>")
        self.assertEqual(format_currency(self.autoescape_context, '11000', 'USD'), "<span class='date'>US$11,000.00</span>")
        self.assertEqual(format_currency(self.autoescape_context, 0), "<span class='date'>£0.00</span>")
        self.assertEqual(format_currency(self.autoescape_context, 0.00), "<span class='date'>£0.00</span>")
        self.assertEqual(format_currency(self.autoescape_context, '', ), "<span class='date'></span>")
        self.assertEqual(format_currency(self.autoescape_context, None), "<span class='date'></span>")
        self.assertEqual(format_currency(self.autoescape_context, Undefined()), "<span class='date'></span>")

    @patch('app.jinja_filters.flask_babel.get_locale', Mock(return_value='en_GB'))
    def test_format_number(self):
        self.assertEqual(format_number(123), '123')
        self.assertEqual(format_number('123.4'), '123.4')
        self.assertEqual(format_number('123.40'), '123.4')
        self.assertEqual(format_number('1000'), '1,000')
        self.assertEqual(format_number('10000'), '10,000')
        self.assertEqual(format_number('100000000'), '100,000,000')
        self.assertEqual(format_number(0), '0')
        self.assertEqual(format_number(0.00), '0')
        self.assertEqual(format_number(''), '')
        self.assertEqual(format_number(None), '')
        self.assertEqual(format_number(Undefined()), '')

    def test_format_multilined_string_matches_carriage_return(self):
        # Given
        new_line = 'this is on a new\rline'

        # When
        format_value = format_multilined_string(self.autoescape_context, new_line)

        self.assertEqual(format_value, 'this is on a new<br>line')

    def test_format_multilined_string_matches_new_line(self):
        # Given
        new_line = 'this is on a new\nline'

        # When
        format_value = format_multilined_string(self.autoescape_context,
                                                new_line)

        self.assertEqual(format_value, 'this is on a new<br>line')

    def test_format_multilined_string_matches_carriage_return_new_line(self):
        # Given
        new_line = 'this is on a new\r\nline'

        # When
        format_value = format_multilined_string(self.autoescape_context, new_line)

        self.assertEqual(format_value, 'this is on a new<br>line')

    def test_format_multilined_string(self):
        # Given
        new_line = 'this is\ron a\nnew\r\nline'

        # When
        format_value = format_multilined_string(self.autoescape_context,
                                                new_line)

        self.assertEqual(format_value, 'this is<br>on a<br>new<br>line')

    def test_format_multilined_string_auto_escape(self):
        # Given
        new_line = '<'

        # When
        format_value = format_multilined_string(self.autoescape_context, new_line)

        self.assertEqual(str(format_value), '&lt;')

    def test_get_current_date(self):
        # Given
        date_format = '%-d %B %Y'

        # When
        format_value = get_current_date(self.autoescape_context)
        current_date = as_london_tz(datetime.utcnow()).strftime(date_format)

        # Then
        self.assertEqual(format_value, "<span class='date'>{date}</span>".format(date=current_date))

    def test_format_date(self):
        # Given
        date = '2017-01-01'

        # When
        with self.app_request_context('/'):
            format_value = format_date(self.autoescape_context, date)

        # Then
        self.assertEqual(format_value, "<span class='date'>1 January 2017</span>")

    def test_format_old_date_does_not_change_timezone(self):
        """ Flask Babel shows some strange behaviour with dates prior to 1902.
        This appears to be because of a bug in pytz relating to 32 bit time_t types
        To avoid it, `datetimes` are converted to `date` objects before being passed
        to `flask_babel.format_date()`.
        """
        date = '1901-01-01'

        with self.app_request_context('/'):
            format_value = format_date(self.autoescape_context, date)

        assert format_value.striptags() == '1 January 1901'

    def test_format_date_month_year(self):
        # Given
        date = '2017-01'

        # When
        with self.app_request_context('/'):
            format_value = format_date(self.autoescape_context, date)

        # Then
        self.assertEqual(format_value, "<span class='date'>January 2017</span>")

    def test_format_date_markup(self):
        # Given
        date = [Markup('2017-01')]

        # When
        with self.app_request_context('/'):
            format_value = format_date(self.autoescape_context, date)

        # Then
        self.assertEqual(format_value, "<span class='date'>January 2017</span>")

    def test_format_date_non_string(self):
        # Given
        date = 123

        # When
        format_value = format_date(self.autoescape_context, date)

        # Then
        self.assertEqual(format_value, 123)

    def test_format_date_none(self):
        # Given
        date = None

        # When
        format_value = format_date(self.autoescape_context, date)

        # Then
        self.assertIsNone(format_value)

    def test_format_date_time_in_bst(self):
        # Given a date after DST started
        date_time = '2018-03-29T11:59:13.528680'

        # When
        with self.app_request_context('/'):
            format_value = format_datetime(self.autoescape_context, date_time)

        # Then
        self.assertEqual(format_value, "<span class='date'>29 March 2018 at 12:59</span>")

    def test_format_date_time_in_gmt(self):
        # Given
        date_time = '2018-10-28T11:59:13.528680'

        # When
        with self.app_request_context('/'):
            format_value = format_datetime(self.autoescape_context, date_time)

        # Then
        self.assertEqual(format_value, "<span class='date'>28 October 2018 at 11:59</span>")

    def test_format_conditional_date_not_date(self):
        # Given       no test for integers this check was removed from jinja_filters

        invalid_input = [('1', None),
                         ('1-1-1', None)]

        # When
        for nonsense in invalid_input:
            date1 = nonsense[0]
            date2 = nonsense[1]
            with self.assertRaises(Exception) as exception:
                format_conditional_date(self.autoescape_context, date1, date2)
            # Then
            self.assertIn("does not match format '%Y-%m'", str(exception.exception))

    def test_format_conditional_date_not_set(self):
        # Given

        # When
        with self.assertRaises(Exception) as exception:
            format_conditional_date(self.autoescape_context, None, None)

        # Then
        self.assertIn('No valid items provided.', str(exception.exception))

    def test_format_conditional_date(self):
        # Given

        datelist = [('2016-01-12', '2016-02-12', '12 January 2016'),
                    ('2017-12-23', None, '23 December 2017'),
                    (None, '2017-12-24', '24 December 2017')]

        # When
        with self.app_request_context('/'):
            for triple in datelist:
                date1 = triple[0]
                date2 = triple[1]

                format_value = format_conditional_date(self.autoescape_context, date1, date2)

                # Then
                self.assertEqual(format_value, "<span class='date'>{date}</span>".format(date=triple[2]))

    def test_calculate_years_difference(self):
        with patch('app.setup.get_session_store', return_value=None):
            # Given
            ten_years_ago = (datetime.today() + relativedelta(years=-10)).strftime('%Y-%m-%d')

            date_list = [('2017-01-30', '2018-01-30', '1 year'),
                         ('2015-02-02', '2018-02-01', '2 years'),
                         ('2016-02-29', '2017-02-28', '1 year'),
                         ('2016-02-29', '2020-02-28', '3 years'),
                         (ten_years_ago, 'now', '10 years')]

            for dates in date_list:
                start_date = dates[0]
                end_date = dates[1]

                # When
                calculated_value = calculate_years_difference(start_date, end_date)

                # Then
                self.assertEqual(calculated_value, dates[2])

    def test_calculate_years_difference_none(self):
        # Given
        with self.assertRaises(Exception) as e:
            # When
            calculate_years_difference(None, '2017-01-17')

        # Then
        self.assertEqual('Valid date(s) not passed to calculate_years_difference filter', str(e.exception))

    def test_format_date_range(self):
        # Given
        start_date = '2017-01-01'
        end_date = '2017-01-31'

        # When
        with self.app_request_context('/'):
            format_value = format_date_range(self.autoescape_context, start_date, end_date)

        # Then
        self.assertEqual(format_value, "<span class='date'>1 January 2017</span> to <span class='date'>31 January 2017</span>")

    def test_format_date_range_missing_end_date(self):
        # Given
        start_date = '2017-01-01'

        # When
        with self.app_request_context('/'):
            format_value = format_date_range(self.autoescape_context, start_date)

        # Then
        self.assertEqual(format_value, "<span class='date'>1 January 2017</span>")

    def test_format_household_name(self):
        # Given
        name = ['John', 'Doe']

        # When
        format_value = format_household_name(name)

        self.assertEqual(format_value, 'John Doe')

    def test_format_household_name_no_surname(self):
        # Given
        name = ['John', '']

        # When
        format_value = format_household_name(name)

        self.assertEqual(format_value, 'John')

    def test_format_household_name_surname_is_none(self):
        # Given
        name = ['John', None]

        # When
        format_value = format_household_name(name)

        self.assertEqual(format_value, 'John')

    def test_format_household_name_no_first_name(self):
        # Given
        name = ['', 'Doe']

        # When
        format_value = format_household_name(name)

        self.assertEqual(format_value, 'Doe')

    def test_format_household_name_first_name_is_none(self):
        # Given
        name = [None, 'Doe']

        # When
        format_value = format_household_name(name)

        self.assertEqual(format_value, 'Doe')

    def test_format_household_name_first_middle_and_last(self):
        # Given
        name = ['John', 'J', 'Doe']

        # When
        format_value = format_household_name(name)

        self.assertEqual(format_value, 'John J Doe')

    def test_format_household_name_no_middle_name(self):
        # Given
        name = ['John', '', 'Doe']

        # When
        format_value = format_household_name(name)

        self.assertEqual(format_value, 'John Doe')

    def test_format_household_name_middle_name_is_none(self):
        # Given
        name = ['John', None, 'Doe']

        # When
        format_value = format_household_name(name)

        self.assertEqual(format_value, 'John Doe')

    def test_format_household_name_trim_spaces(self):
        # Given
        name = ['John  ', '   Doe   ']

        # When
        format_value = format_household_name(name)

        self.assertEqual(format_value, 'John Doe')

    def test_format_household_name_possessive(self):
        # Given
        name = ['John', 'Doe']

        # When
        format_value = format_household_name_possessive(name)

        self.assertEqual(format_value, 'John Doe\u2019s')

    def test_format_household_name_possessive_with_no_names(self):
        # Given
        name = [Undefined(), Undefined()]

        # When
        format_value = format_household_name_possessive(name)

        self.assertIsNone(format_value)

    def test_format_household_name_possessive_trailing_s(self):
        # Given
        name = ['John', 'Does']

        # When
        format_value = format_household_name_possessive(name)

        self.assertEqual(format_value, 'John Does\u2019')

    def test_format_household_summary(self):
        names = [
            ['Alice', 'Bob', '\\', 'Dave'],
            ['', 'Berty', '"', 'Dixon'],
            ['Aardvark', 'Brown', '!', 'Davies']
        ]

        format_value = format_household_summary(self.autoescape_context, names)
        expected_result = '<ul>' \
                          '<li>Alice Aardvark</li>' \
                          '<li>Bob Berty Brown</li>' \
                          '<li>\\ &#34; !</li>' \
                          '<li>Dave Dixon Davies</li>' \
                          '</ul>'

        self.assertEqual(format_value, expected_result)


    def test_concatenated_list(self):
        # Given
        list_items = ['1 The ONS', 'Newport', 'NP108XG']

        # When
        format_value = concatenated_list(list_items)

        self.assertEqual(format_value, '1 The ONS, Newport, NP108XG')

    def test_concatenated_list_one_entry(self):
        # Given
        list_items = ['One entry']

        # When
        format_value = concatenated_list(list_items)

        self.assertEqual(format_value, 'One entry')

    def test_concatenated_list_trim_white_spaces_and_trailing_commas(self):
        # Given
        list_items = ['', '1 The ONS  ', 'Newport  ', '  NP108XG', '']

        # When
        format_value = concatenated_list(list_items)

        self.assertEqual(format_value, '1 The ONS, Newport, NP108XG')

    def test_format_percentage(self):
        self.assertEqual(format_percentage('100'), '100%')
        self.assertEqual(format_percentage(100), '100%')
        self.assertEqual(format_percentage(4.5), '4.5%')

    def test_format_number_to_alphabetic_letter(self):
        self.assertEqual(format_number_to_alphabetic_letter(0), 'a')
        self.assertEqual(format_number_to_alphabetic_letter(4), 'e')
        self.assertEqual(format_number_to_alphabetic_letter(25), 'z')
        self.assertEqual(format_number_to_alphabetic_letter(-1), '')

    @patch('app.jinja_filters.flask_babel.get_locale', Mock(return_value='en_GB'))
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
        self.assertEqual(format_unit('duration-hour', 100), '100 hrs')
        self.assertEqual(format_unit('duration-hour', 100, 'long'), '100 hours')
        self.assertEqual(format_unit('duration-year', 100, 'long'), '100 years')

    @patch('app.jinja_filters.flask_babel.get_locale', Mock(return_value='cy'))
    def test_format_unit_welsh(self):
        self.assertEqual(format_unit('duration-hour', 100), '100 awr')
        self.assertEqual(format_unit('duration-year', 100), '100 bl')
        self.assertEqual(format_unit('duration-hour', 100, 'long'), '100 awr')
        self.assertEqual(format_unit('duration-year', 100, 'long'), '100 mlynedd')

    @patch('app.jinja_filters.flask_babel.get_locale', Mock(return_value='en_GB'))
    def test_format_unit_input_label(self):
        self.assertEqual(format_unit_input_label('length-meter'), 'm')
        self.assertEqual(format_unit_input_label('length-centimeter'), 'cm')
        self.assertEqual(format_unit_input_label('length-mile'), 'mi')
        self.assertEqual(format_unit_input_label('length-kilometer'), 'km')
        self.assertEqual(format_unit_input_label('area-square-meter'), 'm²')
        self.assertEqual(format_unit_input_label('area-square-centimeter'), 'cm²')
        self.assertEqual(format_unit_input_label('area-square-kilometer'), 'km²')
        self.assertEqual(format_unit_input_label('area-square-mile'), 'sq mi')
        self.assertEqual(format_unit_input_label('area-hectare'), 'ha')
        self.assertEqual(format_unit_input_label('area-acre'), 'ac')
        self.assertEqual(format_unit_input_label('volume-cubic-meter'), 'm³')
        self.assertEqual(format_unit_input_label('volume-cubic-centimeter'), 'cm³')
        self.assertEqual(format_unit_input_label('volume-liter'), 'l')
        self.assertEqual(format_unit_input_label('volume-hectoliter'), 'hl')
        self.assertEqual(format_unit_input_label('volume-megaliter'), 'Ml')
        self.assertEqual(format_unit_input_label('duration-hour'), 'hr')
        self.assertEqual(format_unit_input_label('duration-hour', 'long'), 'hours')
        self.assertEqual(format_unit_input_label('duration-year'), 'yr')
        self.assertEqual(format_unit_input_label('duration-year', 'long'), 'years')

    @patch('app.jinja_filters.flask_babel.get_locale', Mock(return_value='cy'))
    def test_format_unit_input_label_welsh(self):
        self.assertEqual(format_unit_input_label('duration-hour'), 'awr')
        self.assertEqual(format_unit_input_label('duration-hour', 'long'), 'awr')
        self.assertEqual(format_unit_input_label('duration-year'), 'bl')
        self.assertEqual(format_unit_input_label('duration-year', 'long'), 'flynedd')

    def test_format_year_month_duration(self):
        with self.app_request_context('/'):
            self.assertEqual(format_duration({'years': 5, 'months': 4}), '5 years 4 months')
            self.assertEqual(format_duration({'years': 5, 'months': 0}), '5 years')
            self.assertEqual(format_duration({'years': 0, 'months': 4}), '4 months')
            self.assertEqual(format_duration({'years': 1, 'months': 1}), '1 year 1 month')
            self.assertEqual(format_duration({'years': 0, 'months': 0}), '0 months')

    def test_format_year_duration(self):
        with self.app_request_context('/'):
            self.assertEqual(format_duration({'years': 5}), '5 years')
            self.assertEqual(format_duration({'years': 1}), '1 year')
            self.assertEqual(format_duration({'years': 0}), '0 years')

    def test_format_month_duration(self):
        with self.app_request_context('/'):
            self.assertEqual(format_duration({'months': 5}), '5 months')
            self.assertEqual(format_duration({'months': 1}), '1 month')
            self.assertEqual(format_duration({'months': 0}), '0 months')

    def test_format_unordered_list(self):
        list_items = [['item 1', 'item 2']]

        formatted_value = format_unordered_list(self.autoescape_context, list_items)

        expected_value = '<ul><li>item 1</li><li>item 2</li></ul>'

        self.assertEqual(expected_value, formatted_value)

    def test_format_unordered_list_with_no_input(self):
        list_items = []

        formatted_value = format_unordered_list(self.autoescape_context, list_items)

        self.assertEqual('', formatted_value)

    def test_format_unordered_list_with_empty_list(self):
        list_items = [[]]

        formatted_value = format_unordered_list(self.autoescape_context, list_items)

        self.assertEqual('', formatted_value)

    def test_format_unordered_list_missing_items(self):
        possible_items = ['item 1', 'item 2', 'item 3', 'item 4']
        list_items = [['item 1', 'item 3']]

        formatted_value = format_unordered_list_missing_items(self.autoescape_context, possible_items, list_items)

        expected_value = '<ul><li>item 2</li><li>item 4</li></ul>'

        self.assertEqual(expected_value, formatted_value)

    def test_format_unordered_list_missing_items_with_no_input(self):
        possible_items = ['item 1', 'item 2']
        list_items = []

        formatted_value = format_unordered_list_missing_items(self.autoescape_context, possible_items, list_items)

        expected_value = '<ul><li>item 1</li><li>item 2</li></ul>'

        self.assertEqual(expected_value, formatted_value)

    def test_format_unordered_list_missing_items_with_empty_list(self):
        possible_items = ['item 1', 'item 2']
        list_items = [[]]

        formatted_value = format_unordered_list_missing_items(self.autoescape_context, possible_items, list_items)

        expected_value = '<ul><li>item 1</li><li>item 2</li></ul>'

        self.assertEqual(expected_value, formatted_value)

    def test_format_unordered_list_missing_items_with_all_selected(self):
        possible_items = ['item 1', 'item 2']
        list_items = [['item 1', 'item 2']]

        formatted_value = format_unordered_list_missing_items(self.autoescape_context, possible_items, list_items)

        self.assertEqual('', formatted_value)

    def test_max_value(self):
        # Given
        two_ints = (1, 2)

        # When
        max_of_two = max_value(*two_ints)

        # Then
        self.assertEqual(max_of_two, 2)

    def test_max_value_none(self):
        # Given
        one_int = (1, None)

        # When
        max_of_two = max_value(*one_int)

        # Then
        self.assertEqual(max_of_two, 1)

    def test_max_value_undefined(self):
        # Given
        args = ('foo', Undefined())

        # When
        with self.assertRaises(Exception) as exception:
            max_value(*args)

        # Then
        self.assertIn(
            "Cannot determine maximum of incompatible types max(<class 'str'>,"
            " <class 'jinja2.runtime.Undefined'>)", str(exception.exception))

    def test_max_values_incompatible(self):
        # Given
        args = (1, 'abc')

        # When
        with self.assertRaises(Exception) as exception:
            max_value(*args)

        # Then
        self.assertIn(
            "Cannot determine maximum of incompatible types max(<class 'int'>,"
            " <class 'str'>)", str(exception.exception))

    def test_max_values_compatible(self):
        # Given
        args = (-1, True)

        # When
        max_of_two = max_value(*args)

        # Then
        self.assertEqual(max_of_two, True)

    def test_max_value_str(self):
        # Given
        two_str = ('a', 'abc')

        # When
        max_of_two = max_value(*two_str)

        # Then
        self.assertEqual(max_of_two, 'abc')

    def test_max_value_date(self):
        # Given
        now = datetime.utcnow()
        then = now - timedelta(seconds=60)
        two_dates = (then, now)

        # When
        max_of_two = max_value(*two_dates)

        # Then
        self.assertEqual(max_of_two, now)

    def test_min_value(self):
        # Given
        two_ints = (1, 2)

        # When
        min_of_two = min_value(*two_ints)

        # Then
        self.assertEqual(min_of_two, 1)

    def test_min_value_none(self):
        # Given
        one_int = (1, None)

        # When
        min_of_two = min_value(*one_int)

        # Then
        self.assertEqual(min_of_two, 1)

    def test_min_value_undefined(self):
        # Given
        args = ('foo', Undefined())

        # When
        with self.assertRaises(Exception) as exception:
            min_value(*args)

        # Then
        self.assertIn(
            "Cannot determine minimum of incompatible types min(<class 'str'>,"
            " <class 'jinja2.runtime.Undefined'>)", str(exception.exception))

    def test_min_values_incompatible(self):
        # Given
        args = (1, 'abc')

        # When
        with self.assertRaises(Exception) as exception:
            min_value(*args)

        # Then
        self.assertIn(
            "Cannot determine minimum of incompatible types min(<class 'int'>,"
            " <class 'str'>)", str(exception.exception))

    def test_min_values_compatible(self):
        # Given
        args = (-1, True)

        # When
        min_of_two = min_value(*args)

        # Then
        self.assertEqual(min_of_two, -1)

    def test_min_value_str(self):
        # Given
        two_str = ('a', 'abc')

        # When
        min_of_two = min_value(*two_str)

        # Then
        self.assertEqual(min_of_two, 'a')

    def test_min_value_date(self):
        # Given
        now = datetime.utcnow()
        then = now - timedelta(seconds=60)
        two_dates = (then, now)

        # When
        min_of_two = min_value(*two_dates)

        # Then
        self.assertEqual(min_of_two, then)

    def test_get_answer_label_with_answer_label(self):
        # Given
        answer_id = 'answer'
        context = SimpleNamespace(
            parent={
                'question': {
                    'id': 'question',
                    'answers': [{
                        'id': 'answer',
                        'label': 'answer_label'
                    }]
                }
            }
        )

        # When
        answer_label = get_answer_label(context, answer_id)

        # Then
        self.assertEqual(answer_label, 'answer_label')

    def test_get_answer_label_with_no_answer_label_and_title(self):
        # Given
        answer_id = 'answer'
        context = SimpleNamespace(
            parent={
                'question': {
                    'id': 'question',
                    'title': 'question_title',
                    'answers': [{
                        'id': 'answer'
                    }]
                }
            }
        )

        # When
        answer_label = get_answer_label(context, answer_id)

        # Then
        self.assertEqual(answer_label, 'question_title')

    def test_offset_date_from_day(self):
        test_cases = [
            # (Input Date, offset, day of week, expected output)
            ('2018-08-10', {}, 'SU', '2018-08-05'),  # Friday outputs previous Sunday
            ('2018-08-05', {}, 'SU', '2018-07-29'),  # Sunday outputs previous Sunday (Must be a full Sunday)
            ('2018-08-06', {}, 'SU', '2018-08-05'),  # Monday outputs previous Sunday
            ('2018-08-06', {'days': -1}, 'SU', '2018-08-04'),  # Previous sunday with -1 day offset
            ('2018-08-05', {'weeks': 1}, 'SU', '2018-08-05'),  # Previous sunday with +1 week offset, back to input
            ('2018-08-10', {}, 'FR', '2018-08-03'),  # Friday outputs previous Friday
            ('2018-08-10T13:32:20.365665', {}, 'FR', '2018-08-03'),  # Ensure we can handle datetime input
            ('2018-08-10', {'weeks': 4}, 'FR', '2018-08-31'),  # Friday outputs previous Friday + 4 weeks
            ('2018-08-10', {'bad_period': 4}, 'FR', '2018-08-03'),  # Friday outputs previous Friday + nothing
            ('2018-08-10', {'years': 1}, 'FR', '2019-08-03'),  # Friday outputs previous Friday + 1 year
            ('2018-08-10', {'years': 1, 'weeks': 1, 'days': 1}, 'FR', '2019-08-11'),  # Friday outputs previous Friday + 1 year + 1 week + 1 day
        ]
        for case in test_cases:
            self.assertEqual(calculate_offset_from_weekday_in_last_whole_week(*case[0:3]), case[3])

    def test_bad_day_of_week_offset_date_from_day(self):
        with self.assertRaises(Exception):
            calculate_offset_from_weekday_in_last_whole_week('2018-08-10', {}, 'BA')

    def test_offset_date_defaults_to_now_if_date_not_passed(self):
        with patch('app.jinja_filters.datetime') as mock_datetime:
            # pylint: disable=unnecessary-lambda
            mock_datetime.utcnow.return_value = datetime(2018, 8, 10)
            mock_datetime.strftime.side_effect = lambda *args, **kw: datetime.strftime(*args, **kw)

            result = calculate_offset_from_weekday_in_last_whole_week(None, {}, 'SU')
            self.assertEqual(result, '2018-08-05')

    def test_format_date_custom(self):
        test_cases = [
            # Input Date, date format, show year
            ('2018-08-14', 'EEEE d MMMM YYYY', 'Tuesday 14 August 2018'),
            ('2018-08-14', 'EEEE d MMMM', 'Tuesday 14 August'),
            ('2018-08-14', 'EEEE d', 'Tuesday 14'),
            ('2018-08-14', 'd MMMM YYYY', '14 August 2018'),
        ]

        with self.app_request_context('/'):
            for case in test_cases:
                self.assertEqual(
                    format_date_custom(self.autoescape_context, *case[0:2]),
                    "<span class='date'>{}</span>".format(case[2])
                )

    def test_format_date_range_no_repeated_month_year(self):
        test_cases = [
            # Start Date, End Date, Date Format, Output Expected First, Output Expected Second
            ('2018-08-14', '2018-08-16', 'EEEE d MMMM YYYY', 'Tuesday 14', 'Thursday 16 August 2018'),
            ('2018-07-31', '2018-08-16', 'EEEE d MMMM YYYY', 'Tuesday 31 July', 'Thursday 16 August 2018'),
            ('2017-12-31', '2018-08-16', 'EEEE d MMMM YYYY', 'Sunday 31 December 2017', 'Thursday 16 August 2018'),
            ('2017-12-31', '2018-08-16', 'MMMM YYYY', 'December 2017', 'August 2018'),
            ('2018-08-14', '2018-08-16', 'MMMM YYYY', 'August 2018', 'August 2018'),
            ('2017-12-31', '2018-08-16', 'YYYY', '2017', '2018'),
            ('2017-07-31', '2018-08-16', 'YYYY', '2017', '2018'),
            ('2018-08-14', '2018-08-16', 'EEEE d', 'Tuesday 14', 'Thursday 16')
        ]

        with self.app_request_context('/'):
            for case in test_cases:
                self.assertEqual(
                    format_date_range_no_repeated_month_year(self.autoescape_context, *case[0:3]),
                    "<span class='date'>{}</span> to <span class='date'>{}</span>".format(case[3], case[4])
                )

    @patch('app.jinja_filters.format_unordered_list')
    def test_format_repeated_summaries_unformatted(self, patched_format):  # pylint: disable=no-self-use

        test_cases = [
            # (input list, expected output)
            ([['John', 'Smith'], [['Jane', 'Sarah'], ['Smith', 'Smythe']]], ['John Smith', 'Jane Smith', 'Sarah Smythe']),
            ([['John', 'Smith']], ['John Smith']),
            ([['John', 'Smith'], ['Andy', 'Smith'], ['David', 'Smith']], ['John Smith', 'Andy Smith', 'David Smith']),
            ([[['Jane', 'Sarah'], ['Smith', 'Smith']]], ['Jane Smith', 'Sarah Smith']),
            ([[['David', 'Sarah'], ['Smith', 'Smith']]], ['David Smith', 'Sarah Smith']),
            ([[['David', 'Sarah'], ['', 'Smith']]], ['David', 'Sarah Smith']),
            ([['John', 'Smith'], [[], []]], ['John Smith'])
        ]

        for case in test_cases:
            format_repeating_summary(None, case[0])
            # Format unordered list takes a list of lists
            patched_format.assert_called_with(None, [[Markup(x) for x in case[1]]])

    def test_format_repeated_summaries_no_input(self):

        self.assertEqual('', format_repeating_summary(None, []))

    def test_format_repeated_summaries_delimiters(self):
        self.autoescape_context = Mock(autoescape=True)
        output = format_repeating_summary(self.autoescape_context, [['', '51 Testing Gardens', '', 'Bristol', 'BS9 1AW']], delimiter=', ')
        self.assertEqual(output, '<ul><li>51 Testing Gardens, Bristol, BS9 1AW</li></ul>')

    def test_format_address_list_undefined_values(self):
        user_entered_address = [Undefined(), Undefined(), Undefined(), Undefined(), Undefined()]
        metadata_address = ['123', 'Testy', 'Place', 'Newport', 'NP5 7AR']
        self.assertEqual('123<br />Testy<br />Place<br />Newport<br />NP5 7AR',
                         format_address_list(user_entered_address, metadata_address))

    def test_format_address_list_missing_values(self):
        user_entered_address = ['44', 'Testing', '', 'Swansea', '']
        metadata_address = ['123', 'Testy', 'Place', 'Newport', 'NP5 7AR']
        self.assertEqual('44<br />Testing<br />Swansea',
                         format_address_list(user_entered_address, metadata_address))

    def test_format_address_list_None_value(self):
        user_entered_address = [None, None, None, None, None]
        metadata_address = [None, None, None, None, None]
        with self.assertRaises(Exception):
            format_address_list(user_entered_address, metadata_address)

    def test_format_address_list_no_values_in_answer(self):
        user_entered_address = ['', '', '', '', '']
        metadata_address = ['123', 'Testy', 'Place', 'Newport', 'NP5 7AR']
        self.assertEqual('123<br />Testy<br />Place<br />Newport<br />NP5 7AR',
                         format_address_list(user_entered_address, metadata_address))

    def test_format_address_list_no_metadata(self):
        user_entered_address = ['44', 'Testing', 'Gardens', 'Swansea', 'SA1 1AA']
        metadata_address = []
        self.assertEqual('44<br />Testing<br />Gardens<br />Swansea<br />SA1 1AA',
                         format_address_list(user_entered_address, metadata_address))

    def test_format_address_list(self):
        user_entered_address = ['44', 'Testing', 'Gardens', 'Swansea', 'SA1 1AA']
        metadata_address = ['123', 'Testy', 'Place', 'Newport', 'NP5 7AR']
        self.assertEqual('44<br />Testing<br />Gardens<br />Swansea<br />SA1 1AA',
                         format_address_list(user_entered_address, metadata_address))

    def test_format_address_list_concatenated_list_no_values(self):
        answer_address = ['', '', '']
        metadata_address = ['', '', '']

        with self.assertRaises(Exception) as error:
            format_address_list(answer_address, metadata_address)

        self.assertEqual('No valid address passed to format_address_list filter', error.exception.args[0])

    def test_first_non_empty_item_filter_returns_first_non_empty_item(self):
        # Given
        expected_actual_scenarios = [
            ['only value', (Markup('only value'),)],
            ['first valid value', (Markup('first valid value'), Markup('second valid value'))],
            ['first valid value', (Markup('first valid value'), Markup('second valid value'), '')],
            ['first valid value', (Markup('first valid value'), Markup('second valid value'), Undefined())],
            ['first valid value', (Markup('first valid value'), Markup('second valid value'), None)],
            ['first valid value', (Markup(''), Markup('first valid value'))],
            ['first valid value', (Undefined(), Markup('first valid value'))],
            ['first valid value', (None, Markup('first valid value'))],
            ['first valid value', (Markup(''), Undefined(), None, Markup('first valid value'))],
            ['False', (None, False, [], {}, (), '', set(), b'', Markup('first valid value'))],
            ['0', (Markup(''), Undefined(), None, Markup('0'))],
            ['0', (0, Markup(''), Undefined(), None, Markup('0'))],
            ['0.0', (0.00, 0, None, Markup('0'))],
            ['0j', ('', 0j, None, Undefined())],
            ['False', ('', False, None, Undefined())]
        ]

        # When
        for scenario in expected_actual_scenarios:
            with self.app_request_context('/'):
                value = first_non_empty_item(self.autoescape_context, *scenario[1])

            # Then
            assert scenario[0] == value

    def test_first_non_empty_item_filter_raises_exception_when_all_empty(self):
        # Given
        scenarios = [
            [(Undefined())],
            [(Undefined(), Undefined())],
            [(None, None)],
            [('', '')],
            [(Undefined(), None, '')],
            [(Undefined(), None, '')],
            [(None, '')],
            [(None, [], {}, (), '', set(), b'')]
        ]

        # When
        for scenario in scenarios:
            with self.assertRaises(Exception) as exception:
                with self.app_request_context('/'):
                    first_non_empty_item(self.autoescape_context, *scenario[0])

            # Then
            assert 'No valid items provided.' in str(exception.exception)
