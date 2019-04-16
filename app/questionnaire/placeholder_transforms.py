from datetime import datetime

from dateutil.relativedelta import relativedelta
from dateutil.tz import tzutc

from babel.numbers import format_currency
from babel.dates import format_datetime
from babel import numbers

from app.settings import DEFAULT_LOCALE


class PlaceholderTransforms:
    """
    A class to group the transforms that can be used within placeholders
    """

    def __init__(self, language):
        self.language = language

    locale = DEFAULT_LOCALE
    input_date_format = '%Y-%m-%d'
    input_date_format_month_year_only = '%Y-%m'

    def format_currency(self, number=None, currency='GBP'):
        return format_currency(number, currency, locale=self.locale)

    def format_date(self, date_to_format, date_format):
        date_to_format = datetime.strptime(date_to_format, self.input_date_format)
        return format_datetime(date_to_format, date_format, locale=self.locale)

    @staticmethod
    def format_list(list_to_format):
        formatted_list = '<ul>'
        for item in list_to_format:
            formatted_list += '<li>{}</li>'.format(item)
        formatted_list += '</ul>'

        return formatted_list

    @staticmethod
    def remove_empty_from_list(list_to_filter):
        """
        :param list_to_filter: anything that is iterable
        :return: a list with no empty values

        In this filter the following values are considered non empty:
        - None
        - any empty sequence, for example, '', (), [].
        - any empty mapping, for example, {}.

        This filter will treat zero of any numeric type for example, 0, 0.0, 0j and boolean 'False'
        as a valid item since they are naturally 'falsy' in Python but not empty.

        Note: Booleans are a subtype of integers. Zero of any numeric type 'is not False' but 'equals False'.
        Reference: https://docs.python.org/release/3.4.2/library/stdtypes.html?highlight=boolean#boolean-values
        """
        return [item for item in list_to_filter if item or item is False or item == 0]

    def concatenate_list(self, list_to_concatenate, delimiter):
        filtered_list = self.remove_empty_from_list(list_to_concatenate)
        return delimiter.join(filtered_list)

    def format_possessive(self, string_to_format):
        if string_to_format and self.language == 'en':
            lowered_string = string_to_format.lower()

            if lowered_string.endswith("'s") or lowered_string.endswith('’s'):
                return string_to_format[:-2] + '’s'

            if lowered_string[-1:] == 's':
                return string_to_format + '’'

            return string_to_format + '’s'

        return string_to_format

    @staticmethod
    def format_number(number):
        if number or number == 0:
            return numbers.format_decimal(number, locale=PlaceholderTransforms.locale)

        return ''

    @staticmethod
    def calculate_years_difference(first_date, second_date):
        return str(relativedelta(PlaceholderTransforms.parse_date(second_date),
                                 PlaceholderTransforms.parse_date(first_date)).years)

    @staticmethod
    def parse_date(date):
        """
        :param date: string representing a date
        :return: datetime of that date

        Convert `date` from string into `datetime` object. `date` can be 'YYYY-MM-DD', 'YYYY-MM'
        or 'now'. Note that in the shorthand YYYY-MM format, day_of_month is assumed to be 1.
        """
        if date == 'now':
            return datetime.now(tz=tzutc())

        try:
            return datetime.strptime(date, PlaceholderTransforms.input_date_format)\
                .replace(tzinfo=tzutc())
        except ValueError:
            return datetime.strptime(date, PlaceholderTransforms.input_date_format_month_year_only)\
                .replace(tzinfo=tzutc())

    def first_non_empty_item(self, items):
        """
        :param items: anything that is iterable
        :return: first non empty value

         Note: to guarantee the returned element is actually the first non empty element in the iterable,
        'items' must be a data structure that preserves order, ie tuple, list etc.
        If order is not important, this can be reused to return `one of` the elements which is non empty.
        """
        for item in self.remove_empty_from_list(items):
            return item

        return ''
