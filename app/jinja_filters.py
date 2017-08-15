# coding: utf-8

import re
import string

from datetime import datetime

import flask

from jinja2 import Markup, escape, evalcontextfilter

from babel import units

blueprint = flask.Blueprint('filters', __name__)


@blueprint.app_template_filter()
def format_currency(value):
    if value is not None and len(str(value)) > 0:
        return "£{:,.2f}".format(value)
    else:
        return ""


@blueprint.app_template_filter()
def format_percentage(value):
    return "{}%".format(value)


def format_unit(unit, value=''):
    return units.format_unit(value=value, measurement_unit=unit, length="short", locale='en_GB')


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
def format_date(value):
    return value.strftime('%-d %B %Y')


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
        raise Exception("No valid dates passed to format_conditional_dates filter")

    if isinstance(date, datetime):
        return format_date(date)
    else:
        return format_date(datetime.strptime(date, "%d/%m/%Y"))


def format_str_as_short_date(value):
    return datetime.strptime(value, "%d/%m/%Y").strftime('%d %B %Y')


def format_start_end_date(start_date, end_date=None):
    if end_date:
        return '{from_date} to {to_date}'.format(from_date=start_date.strftime('%-d %B %Y'),
                                                 to_date=end_date.strftime('%-d %B %Y'))
    return format_date(start_date)


@blueprint.app_template_filter()
def format_str_as_date_range(value):
    from_date = format_str_as_short_date(value['from'])
    to_date = format_str_as_short_date(value['to'])
    return '{from_date} to {to_date}'.format(from_date=from_date, to_date=to_date)


@blueprint.app_template_filter()
def format_str_as_month_year_date(value):
    return datetime.strptime(value, "%m/%Y").strftime('%B %Y')


@blueprint.app_template_filter()
def format_str_as_date(value):
    return format_str_as_short_date(value)


@blueprint.app_template_filter()
def format_household_member_name(names):
    return ' '.join(map(lambda name: name.strip(), filter(None, names)))


@blueprint.app_template_filter()
def format_household_summary(names):
    if len(names) > 0:
        person_list = '<ul>'
        for first_name, middle_name, last_name in zip(names[0], names[1], names[2]):
            person_list += '<li>{}</li>'.format(format_household_member_name([first_name, middle_name, last_name]))
        person_list += '</ul>'

        return person_list
    return ''


@blueprint.app_template_filter()
def format_number_to_alphabetic_letter(number):
    if int(number) >= 0 and int(number) < 26:
        return string.ascii_lowercase[int(number)]
    return ''


@blueprint.app_context_processor
def start_end_date_check():
    return dict(format_start_end_date=format_start_end_date)


@blueprint.app_context_processor
def conditional_dates_check():
    return dict(format_conditional_date=format_conditional_date)


@blueprint.app_context_processor
def format_unit_processor():
    return dict(format_unit=format_unit)
