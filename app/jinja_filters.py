import re
import string

from datetime import datetime

import flask

from jinja2 import Markup, escape, evalcontextfilter

blueprint = flask.Blueprint('filters', __name__)


@blueprint.app_template_filter()
def format_currency(value):
    if value is not None and len(str(value)) > 0:
        return "£{:,}".format(value)
    else:
        return ""


@blueprint.app_template_filter()
def format_percentage(value):
    return "{}%".format(value)


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
def utility_processor():
    return dict(format_start_end_date=format_start_end_date)
