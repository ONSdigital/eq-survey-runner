# coding: utf-8

import re
import string

from datetime import datetime

import flask

from jinja2 import Markup, escape, evalcontextfilter
from babel import units, numbers

from app.settings import DEFAULT_LOCALE

blueprint = flask.Blueprint('filters', __name__)


@blueprint.app_template_filter()
def format_number(value):
    if value is None or value == '':
        return ''
    return numbers.format_number(value, locale=DEFAULT_LOCALE)


@blueprint.app_template_filter()
def format_currency(value, currency='GBP'):
    if value is None or value == '':
        return ''
    return numbers.format_currency(number=value, currency=currency, locale=DEFAULT_LOCALE)


@blueprint.app_template_filter()
def get_currency_symbol(currency='GBP'):
    return numbers.get_currency_symbol(currency, locale=DEFAULT_LOCALE)


@blueprint.app_template_filter()
def format_currency_for_input(value, decimal_places=0):
    if value is None or value == '':
        return ''
    if decimal_places is None or decimal_places == 0:
        return format_number(value)
    return format_currency(value).replace(get_currency_symbol(), '')


@blueprint.app_template_filter()
def format_percentage(value):
    return '{}%'.format(value)


def format_unit(unit, value=''):
    return units.format_unit(value=value, measurement_unit=unit, length='short', locale=DEFAULT_LOCALE)


@evalcontextfilter
@blueprint.app_template_filter()
def format_multilined_string(context, value):
    escaped_value = escape(value)
    new_line_regex = r'(?:\r\n|\r|\n)+'
    value_with_line_break_tag = re.sub(new_line_regex, '<br>', escaped_value)
    result = '<p>{}</p>'.format(value_with_line_break_tag)

    if context.autoescape:
        return Markup(result)
    return result


@blueprint.app_template_filter()
def format_date(value, date_format='%-d %B %Y'):
    return "<span class='date'>{date}</span>".format(date=datetime.strptime(value, '%Y-%m-%d').strftime(date_format))


@blueprint.app_template_filter()
def format_month_year_date(value, date_format='%B %Y'):
    return "<span class='date'>{date}</span>".format(date=datetime.strptime(value, '%Y-%m').strftime(date_format))


@blueprint.app_template_filter()
def format_datetime(value, date_format='%d %B %Y at %H:%M'):
    return "<span class='date'>{date}</span>".format(date=datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f').strftime(date_format))


@blueprint.app_template_filter()
def format_conditional_date(date1=None, date2=None):
    """
    This function format_conditional_date accepts two dates, a user submitted date and a metadata date

    :param date1 user entered date
    :param date2 is metadata date
    :return: the value of the date to be piped
    """
    if date1:
        date = date1
    else:
        date = date2

    if date is None:
        raise Exception('No valid dates passed to format_conditional_dates filter')

    return format_date(date)


def format_date_range(start_date, end_date=None):
    if end_date:
        return '{from_date} to {to_date}'.format(from_date=format_date(start_date),
                                                 to_date=format_date(end_date))
    return format_date(start_date)


@blueprint.app_template_filter()
def format_household_member_name(names):
    return concatenated_list(list_items=names, delimiter=' ')


@blueprint.app_template_filter()
def format_household_member_name_possessive(names):
    name = format_household_member_name(names)
    last_char = name[-1:]
    if last_char.lower() == 's':
        return name + '’'

    return name + '’s'


@blueprint.app_template_filter()
def format_unordered_list(list_items):
    summary_list = ''

    if list_items and list_items[0]:
        summary_list = '<ul>'
        for item in list_items[0]:
            summary_list += '<li>{}</li>'.format(item)
        summary_list += '</ul>'

    return summary_list


@blueprint.app_template_filter()
def concatenated_list(list_items, delimiter=', '):
    return delimiter.join(map(lambda item: item.strip(), filter(None, list_items)))


@blueprint.app_template_filter()
def format_household_summary(names):
    if names:
        person_list = []
        for first_name, middle_name, last_name in zip(names[0], names[1], names[2]):
            person_list.append(format_household_member_name([first_name, middle_name, last_name]))

        return format_unordered_list([person_list])
    return ''


@blueprint.app_template_filter()
def format_number_to_alphabetic_letter(number):
    if 0 <= int(number) < 26:
        return string.ascii_lowercase[int(number)]
    return ''


@blueprint.app_context_processor
def start_end_date_check():
    return dict(format_date_range=format_date_range)


@blueprint.app_context_processor
def conditional_dates_check():
    return dict(format_conditional_date=format_conditional_date)


@blueprint.app_context_processor
def format_unit_processor():
    return dict(format_unit=format_unit)


@blueprint.app_context_processor
def format_currency_processor():
    return dict(format_currency=format_currency)


@blueprint.app_context_processor
def get_currency_symbol_processor():
    return dict(get_currency_symbol=get_currency_symbol)


@blueprint.app_context_processor
def format_currency_for_input_processor():
    return dict(format_currency_for_input=format_currency_for_input)


@blueprint.app_context_processor
def format_number_processor():
    return dict(format_number=format_number)
