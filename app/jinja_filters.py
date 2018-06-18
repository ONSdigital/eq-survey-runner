# coding: utf-8
import re
import string

from datetime import datetime
from dateutil import relativedelta, tz
from babel.dates import format_date

import flask

from jinja2 import Markup, escape, evalcontextfilter, evalcontextfunction, contextfunction
from jinja2.exceptions import UndefinedError

from babel import units, numbers, dates

from app.settings import DEFAULT_LOCALE, BABEL_DEFAULT_LOCALE
from app.questionnaire.rules import convert_to_datetime
blueprint = flask.Blueprint('filters', __name__)

DATE_FORMAT = '%-d %B %Y'


@blueprint.app_template_filter()
def format_number(value):
    if value or value is 0:
        return numbers.format_decimal(value, locale=DEFAULT_LOCALE)
    return ''


@blueprint.app_template_filter()
def format_currency(value, currency='GBP'):
    if value or value is 0:
        return numbers.format_currency(number=value, currency=currency, locale=DEFAULT_LOCALE)
    return ''


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


def as_london_tz(value):
    return value.replace(tzinfo=tz.gettz('UTC')).astimezone(tz.gettz('Europe/London'))


@evalcontextfilter
@blueprint.app_template_filter()
def format_multilined_string(context, value):
    escaped_value = escape(value)
    new_line_regex = r'(?:\r\n|\r|\n)+'
    value_with_line_break_tag = re.sub(new_line_regex, '<br>', escaped_value)
    result = '<p>{}</p>'.format(value_with_line_break_tag)

    return mark_safe(context, result)


@evalcontextfunction
@blueprint.app_template_filter()
def get_current_date(context):
    now = as_london_tz(datetime.utcnow()).strftime(DATE_FORMAT)
    result = "<span class='date'>{date}</span>".format(date=now)
    return mark_safe(context, result)


@evalcontextfilter
@blueprint.app_template_filter()
def format_date(context, value):
    """Format a datetime string.

    :param (jinja2.nodes.EvalContext) context: Evaluation context.
    :param (any) value: Value representing a datetime.
    :returns (str): Formatted datetime.
    """
    value = value[0] if isinstance(value, list) else value
    if not isinstance(value, str):
        return value
    date_format = 'd MMMM YYYY'
    if value and re.match(r'\d{4}-\d{2}$', value):
        date_format = 'MMMM YYYY'
    if value and re.match(r'\d{4}$', value):
        date_format = 'YYYY'
    result = "<span class='date'>{date}</span>".format(
        date=dates.format_date(convert_to_datetime(value), format=date_format, locale=BABEL_DEFAULT_LOCALE))
    return mark_safe(context, result)


@evalcontextfilter
@blueprint.app_template_filter()
def format_datetime(context, value, date_format='d MMMM YYYY' + ' at HH:MM'):

    london_date_time = as_london_tz(datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f'))
    result = "<span class='date'>{date}</span>".format(date=dates.format_datetime(london_date_time, format=date_format, locale=BABEL_DEFAULT_LOCALE))
    return mark_safe(context, result)


@evalcontextfunction
@blueprint.app_template_filter()
def format_conditional_date(context, date1=None, date2=None):
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

    return format_date(context, date)


@blueprint.app_template_filter()
def calculate_years_difference(from_str, to_str):
    if from_str is None or to_str is None:
        raise Exception('Valid date(s) not passed to calculate_years_difference filter')

    to_date = datetime.now() if to_str == 'now' else convert_to_datetime(to_str)
    from_date = convert_to_datetime(from_str)
    difference = relativedelta.relativedelta(to_date, from_date)
    year_string = '{} year' if difference.years == 1 else '{} years'

    return year_string.format(difference.years)


@evalcontextfunction
def format_date_range(context, start_date, end_date=None):
    if end_date:
        result = '{from_date} to {to_date}'.format(from_date=format_date(context, start_date),
                                                   to_date=format_date(context, end_date))
    else:
        result = format_date(context, start_date)

    return mark_safe(context, result)


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


@evalcontextfilter
@blueprint.app_template_filter()
def format_unordered_list(context, list_items):
    summary_list = ''

    if list_items and list_items[0]:
        summary_list = '<ul>'
        for item in list_items[0]:
            summary_list += '<li>{}</li>'.format(item)
        summary_list += '</ul>'

    return mark_safe(context, summary_list)


@blueprint.app_template_filter()
def concatenated_list(list_items, delimiter=', '):
    return Markup(delimiter).join(item.strip() for item in list_items if item)


@evalcontextfilter
@blueprint.app_template_filter()
def format_household_summary(context, names):
    if names:
        person_list = []
        for first_name, middle_name, last_name in zip(names[0], names[1], names[2]):
            person_list.append(format_household_member_name([first_name, middle_name, last_name]))

        return format_unordered_list(context, [person_list])
    return ''


@blueprint.app_template_filter()
def format_number_to_alphabetic_letter(number):
    if 0 <= int(number) < 26:
        return string.ascii_lowercase[int(number)]
    return ''


@blueprint.app_template_filter()
def min_value(a, b):
    try:
        return min(i for i in [a, b] if i is not None)
    except (TypeError, UndefinedError):
        msg = ('Cannot determine minimum of incompatible types '
               'min({}, {})'.format(a.__class__, b.__class__))
        raise Exception(msg)


@blueprint.app_template_filter()
def max_value(a, b):
    try:
        return max(i for i in [a, b] if i is not None)
    except (TypeError, UndefinedError):
        msg = ('Cannot determine maximum of incompatible types '
               'max({}, {})'.format(a.__class__, b.__class__))
        raise Exception(msg)


@contextfunction
@blueprint.app_template_filter()
def get_question_title(context, question_id):
    """Return the value that should be used as the title to a question
    May be from question.title or question_titles in the context"""
    context = context.parent
    question = context['question']

    if question_id == question['id']:
        if question.get('title') is not None:
            return question['title']
        question_title = context['content']['question_titles']
        return question_title[question_id]


@contextfunction
@blueprint.app_template_filter()
def get_answer_label(context, answer_id, question_id):
    """Return the value that should be used as the answer label tries
    answer.label first then resorts to question title"""
    parent_context = context.parent
    question = parent_context['question']
    answers = question['answers']

    for answer in answers:
        if answer_id == answer['id']:
            if answer.get('label') is not None:
                return answer['label']
            return get_question_title(context, question_id)


@blueprint.app_context_processor
def get_current_date_processor():
    return dict(get_current_date=get_current_date)


@blueprint.app_context_processor
def get_question_title_processor():
    return dict(get_question_title=get_question_title)


@blueprint.app_context_processor
def get_answer_label_processor():
    return dict(get_answer_label=get_answer_label)


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


def mark_safe(context, value):
    if context.autoescape:
        value = Markup(value)
    return value
