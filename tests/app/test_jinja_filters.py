# coding: utf-8
from types import SimpleNamespace
from unittest.mock import patch

from jinja2 import Undefined, Markup
from mock import Mock

from app.jinja_filters import (
    format_date, get_currency_symbol,
    format_multilined_string, format_percentage, format_date_range,
    format_datetime,
    format_unit,
    format_number,
    format_unit_input_label, get_answer_label,
    format_duration, get_formatted_currency)
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

    def test_format_percentage(self):
        self.assertEqual(format_percentage('100'), '100%')
        self.assertEqual(format_percentage(100), '100%')
        self.assertEqual(format_percentage(4.5), '4.5%')

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

    def test_get_formatted_currency_with_no_value(self):
        self.assertEqual(get_formatted_currency(''), '')
