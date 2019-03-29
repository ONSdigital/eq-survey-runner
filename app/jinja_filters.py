# coding: utf-8
import re
from datetime import datetime

import flask
import flask_babel
from babel import units, numbers
from jinja2 import Markup, contextfunction, escape, evalcontextfilter, evalcontextfunction

from app.questionnaire.rules import convert_to_datetime

blueprint = flask.Blueprint('filters', __name__)


@blueprint.app_template_filter()
def format_number(value):
    if value or value == 0:
        return numbers.format_decimal(value, locale=flask_babel.get_locale())

    return ''


@evalcontextfunction
def format_currency(context, value, currency='GBP'):
    currency_value = get_formatted_currency(value, currency)
    result = "<span class='date'>{currency_value}</span>".format(currency_value=currency_value)
    return mark_safe(context, result)


def get_formatted_currency(value, currency='GBP'):
    if value or value == 0:
        return numbers.format_currency(number=value, currency=currency, locale=flask_babel.get_locale())

    return ''


@blueprint.app_template_filter()
def get_currency_symbol(currency='GBP'):
    return numbers.get_currency_symbol(currency, locale=flask_babel.get_locale())


@blueprint.app_template_filter()
def format_percentage(value):
    return '{}%'.format(value)


def format_unit(unit, value, length='short'):
    return units.format_unit(value=value, measurement_unit=unit, length=length, locale=flask_babel.get_locale())


def format_unit_input_label(unit, unit_length='short'):
    """
    This function is used to only get the unit of measurement text.  If the unit_length
    is long then only the plural form of the word is returned (e.g., Hours, Years, etc).

    :param (str) unit unit of measurement
    :param (str) unit_length length of unit text, can be one of short/long/narrow
    """
    if unit_length == 'long':
        return units.format_unit(value=2, measurement_unit=unit, length=unit_length, locale=flask_babel.get_locale()).replace('2 ', '')
    return units.format_unit(value='', measurement_unit=unit, length=unit_length, locale=flask_babel.get_locale()).strip()


def format_duration(value):
    parts = []

    if 'years' in value and (value['years'] > 0 or len(value) == 1):
        parts.append(flask_babel.ngettext('%(num)s year', '%(num)s years', value['years']))
    if 'months' in value and (value['months'] > 0 or len(value) == 1 or ('years' in value and value['years'] == 0)):
        parts.append(flask_babel.ngettext('%(num)s month', '%(num)s months', value['months']))
    return ' '.join(parts)


@evalcontextfilter
@blueprint.app_template_filter()
def format_multilined_string(context, value):
    escaped_value = escape(value)
    new_line_regex = r'(?:\r\n|\r|\n)+'
    value_with_line_break_tag = re.sub(new_line_regex, '<br>', escaped_value)
    result = '{}'.format(value_with_line_break_tag)
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

    date_to_format = convert_to_datetime(value).date()
    result = "<span class='date'>{date}</span>".format(
        date=flask_babel.format_date(date_to_format, format=date_format))

    return mark_safe(context, result)


@evalcontextfilter
@blueprint.app_template_filter()
def format_datetime(context, value):

    london_date_time = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
    london_date = london_date_time.date()
    formatted_date = flask_babel.format_date(london_date, format='d MMMM YYYY')
    formatted_time = flask_babel.format_time(london_date_time, format='HH:mm')

    result = "<span class='date'>{date}</span>".format(
        date=flask_babel.gettext('%(date)s at %(time)s', date=formatted_date, time=formatted_time),
    )
    return mark_safe(context, result)


@evalcontextfunction
def format_date_range(context, start_date, end_date=None):
    if end_date:
        result = flask_babel.gettext('%(from_date)s to %(to_date)s',
                                     from_date=format_date(context, start_date),
                                     to_date=format_date(context, end_date))
    else:
        result = format_date(context, start_date)

    return mark_safe(context, result)


@blueprint.app_template_filter()
def answer_is_type(answer, target_answer_type):
    """
    :param answer:
    :param target_answer_type:
    :return: true if the answer type matches given input
    'RepeatingAnswer' question type return 'answers' as an object, and dict for all other question types.
    """
    answer_type = answer['type'] if isinstance(answer, dict) else answer.type
    return answer_type == target_answer_type.lower()


@blueprint.app_template_filter()
def language_urls(languages, current_language):
    return [language for language in languages if language[0] != current_language]


@contextfunction
@blueprint.app_template_filter()
def get_answer_label(context, answer_id):
    """Return the value that should be used as the answer label tries
    answer.label first then resorts to question title"""
    parent_context = context.parent
    question = parent_context['question']
    answers = question['answers']

    for answer in answers:
        if answer_id == answer['id']:
            if answer.get('label') is not None:
                return answer['label']
            return question['title']


@blueprint.app_context_processor
def get_answer_label_processor():
    return dict(get_answer_label=get_answer_label)


@blueprint.app_context_processor
def answer_is_type_processor():
    return dict(answer_is_type=answer_is_type)


@blueprint.app_context_processor
def start_end_date_check():
    return dict(format_date_range=format_date_range)


@blueprint.app_context_processor
def format_unit_processor():
    return dict(format_unit=format_unit)


@blueprint.app_context_processor
def format_unit_input_label_processor():
    return dict(format_unit_input_label=format_unit_input_label)


@blueprint.app_context_processor
def format_duration_processor():
    return dict(format_duration=format_duration)


@blueprint.app_context_processor
def format_currency_processor():
    return dict(format_currency=format_currency)


@blueprint.app_context_processor
def get_currency_symbol_processor():
    return dict(get_currency_symbol=get_currency_symbol)


@blueprint.app_context_processor
def format_number_processor():
    return dict(format_number=format_number)


@blueprint.app_context_processor
def language_urls_processor():
    return dict(language_urls=language_urls)


def mark_safe(context, value):
    if context.autoescape:
        value = Markup(value)
    return value
