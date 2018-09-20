# coding: utf-8
import re
import string
from datetime import datetime

import flask
import flask_babel
from dateutil import relativedelta, tz
from jinja2 import Markup, contextfunction, escape, evalcontextfilter, evalcontextfunction, Undefined
from jinja2.exceptions import UndefinedError

from babel import units, numbers

from app.questionnaire.rules import convert_to_datetime
from app.settings import DEFAULT_LOCALE

blueprint = flask.Blueprint('filters', __name__)


@blueprint.app_template_filter()
def format_number(value):
    if value or value == 0:
        return numbers.format_decimal(value, locale=DEFAULT_LOCALE)

    return ''


@evalcontextfunction
def format_currency(context, value, currency='GBP'):
    currency_value = get_formatted_currency(value, currency)
    result = "<span class='date'>{currency_value}</span>".format(currency_value=currency_value)
    return mark_safe(context, result)


def get_formatted_currency(value, currency='GBP'):
    if value or value == 0:
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
    return get_formatted_currency(value).replace(get_currency_symbol(), '')


@blueprint.app_template_filter()
def format_percentage(value):
    return '{}%'.format(value)


@blueprint.app_template_filter()
def format_address_list(user_entered_address=None, metadata_address=None):
    """
        This function format_address_list accepts two addresses, a user submitted address and a metadata address
        If all the items in address list are 'Undefined' (nothing in answer_store) then we retrieve the metadata.

        :param user_entered_address user entered address which is a list of answer fields
        :param metadata_address metadata address which is a list of answer fields passed to us
        :return: the value of the address to be piped
    """
    if all(isinstance(field, Undefined) for field in user_entered_address) or \
       all(field == '' for field in user_entered_address):
        address = metadata_address
    else:
        address = user_entered_address

    address_list = concatenated_list(list_items=address, delimiter='<br />')

    if not address_list:
        raise Exception('No valid address passed to format_address_list filter')

    return address_list


def format_unit(unit, value='', length='short'):
    return units.format_unit(value=value, measurement_unit=unit, length=length, locale=DEFAULT_LOCALE)


def format_duration(value):
    parts = []

    if 'years' in value and (value['years'] > 0 or len(value) == 1):
        parts.append(flask_babel.ngettext('%(num)s year', '%(num)s years', value['years']))
    if 'months' in value and (value['months'] > 0 or len(value) == 1 or ('years' in value and value['years'] == 0)):
        parts.append(flask_babel.ngettext('%(num)s month', '%(num)s months', value['months']))
    return ' '.join(parts)


def as_london_tz(value):
    return value.replace(tzinfo=tz.gettz('UTC')).astimezone(tz.gettz('Europe/London'))


@evalcontextfilter
@blueprint.app_template_filter()
def format_multilined_string(context, value):
    escaped_value = escape(value)
    new_line_regex = r'(?:\r\n|\r|\n)+'
    value_with_line_break_tag = re.sub(new_line_regex, '<br>', escaped_value)
    result = '{}'.format(value_with_line_break_tag)
    return mark_safe(context, result)


@evalcontextfunction
@blueprint.app_template_filter()
def get_current_date(context):
    now = as_london_tz(datetime.utcnow()).strftime('%-d %B %Y')
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
        date=flask_babel.format_date(convert_to_datetime(value), format=date_format))

    return mark_safe(context, result)


@evalcontextfilter
@blueprint.app_template_filter()
def format_date_custom(context, value, date_format='EEEE d MMMM YYYY'):

    london_date = datetime.strptime(value, '%Y-%m-%d')
    result = "<span class='date'>{date}</span>".format(date=flask_babel.format_datetime(london_date,
                                                                                        format=date_format))
    return mark_safe(context, result)


@evalcontextfilter
@blueprint.app_template_filter()
def format_datetime(context, value, date_format="d MMMM YYYY 'at' HH:mm"):

    london_date_time = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
    result = "<span class='date'>{date}</span>".format(date=flask_babel.format_datetime(london_date_time,
                                                                                        format=date_format))
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
def calculate_offset_from_weekday_in_last_whole_week(input_datetime, offset, day_of_week='MO'):
    """
    Offset a date from a particular day of the week in the previous week.

    Intended to be used to generate reference date ranges around a particular date
    The offsets will always be based on one day of the week in the previous Mon-Sun

    :param (str) input_datetime: The datetime (or date) to offset. Defaults to now
    :param (int) offset: The offset dictionary, can contain days, weeks, or years
    :param (str) day_of_week: The day of the previous week to offset from (two letter abbreviation)
    :returns (str): The offset date
    """
    if input_datetime:
        parsed_datetime = datetime.strptime(input_datetime.split('T')[0], '%Y-%m-%d')
    else:
        parsed_datetime = datetime.utcnow()

    offset_days = offset.get('days', 0)
    offset_weeks = offset.get('weeks', 0)
    offset_years = offset.get('years', 0)

    offset = relativedelta.relativedelta(days=offset_days, weeks=offset_weeks, years=offset_years)

    weekdays = ('MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU')

    try:
        day_of_week_index = weekdays.index(day_of_week)
    except ValueError:
        raise Exception('Invalid day of week passed to calculate_offset_from_weekday_in_last_whole_week')

    day_of_week_offset = relativedelta.relativedelta(days=(-parsed_datetime.weekday() - (7 - day_of_week_index)))
    day_of_last_week = parsed_datetime + day_of_week_offset

    offset_output = day_of_last_week + offset

    return datetime.strftime(offset_output, '%Y-%m-%d')


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


@evalcontextfunction
def format_date_range_no_repeated_month_year(context, start_date, end_date, date_format='d MMMM YYYY'):
    """
    Format a date range, ensuring months and years are not repeated.

    If the dates are in the same year, the first year (YYYY) will be removed.
    If the dates are in the same month and year, the first year (YYYY) and month will be removed.

    e.g. Friday 1 to Sunday 3 October
    or   Thursday 30 September to Sunday 3 October

    Assumptions:
        - The date format uses space as a seperator
        - The date format can have leading and trailing whitespace stripped

    :param (jinja2.nodes.EvalContext) context: Evaluation context.
    :param (str) start_date : The date format that should be used for output. MMMM, YYYY will be removed if necessary
    :param (str) end_date: The date format that should be used for output. MMMM, YYYY will be removed if necessary
    :param (str) date_format: The date format that should be used for output. MMMM, YYYY will be removed if necessary
    :returns (str): The formatted range.
    """
    start_datetime = convert_to_datetime(start_date)
    end_datetime = convert_to_datetime(end_date)

    first_date_format = date_format

    if start_datetime.year == end_datetime.year:
        first_date_format = date_format.replace('YYYY', '')

        if start_datetime.month == end_datetime.month:
            first_date_format = first_date_format.replace('MMMM', '')

    # Cleanup any extra spaces in the new format string
    first_date_format = first_date_format.replace('  ', ' ').strip()

    if not first_date_format:
        # If the date format was entirely removed, leave it alone
        first_date_format = date_format

    output = '{} to {}'.format(
        format_date_custom(context, start_date, first_date_format),
        format_date_custom(context, end_date, date_format),
    )

    return mark_safe(context, output)


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
def answer_is_type(answer, target_answer_type):
    """
    :param answer:
    :param target_answer_type:
    :return: true if the answer type matches given input
    'RepeatingAnswer' question type return 'answers' as an object, and dict for all other question types.
    """
    answer_type = answer['type'] if isinstance(answer, dict) else answer.type
    return answer_type == target_answer_type.lower()


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


@evalcontextfilter
@blueprint.app_template_filter()
def format_repeating_summary(context, items, delimiter=' '):
    """
    Formats a summary from the input list using the provided delimiter
    Input should be a list of lists.
    If there is a third level of lists, these will be zipped together
    e.g.
    [['John', 'Smith'], [['Jane', 'Sarah'], ['Smith', 'Smith']]]
    Should output a list for:
    - John Smith
    - Jane Smith
    - Sarah Smith
    """
    if items:
        intermediates = []
        for item in items:
            if item and isinstance(item[0], list):
                intermediates.extend(list(map(list, zip(*item))))
            else:
                intermediates.append(item)
        output = [concatenated_list(x, delimiter=delimiter) for x in intermediates]
        return format_unordered_list(context, [output])
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


@blueprint.app_template_filter()
def language_urls(languages, current_language):
    return [language for language in languages if language[0] != current_language]


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
def get_question_title_processor():
    return dict(get_question_title=get_question_title)


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
def conditional_dates_check():
    return dict(format_conditional_date=format_conditional_date)


@blueprint.app_context_processor
def format_unit_processor():
    return dict(format_unit=format_unit)


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
def format_currency_for_input_processor():
    return dict(format_currency_for_input=format_currency_for_input)


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
