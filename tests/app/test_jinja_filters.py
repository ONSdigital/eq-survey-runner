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
    max_value, min_value, get_question_title, get_answer_label,
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
