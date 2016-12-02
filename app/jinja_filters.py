import re

from datetime import datetime

import flask

from jinja2 import Markup, escape, evalcontextfilter

blueprint = flask.Blueprint('filters', __name__)


@blueprint.app_template_filter()
def format_currency(value):
    return "£{:,}".format(value)


@evalcontextfilter
@blueprint.app_template_filter()
def nl2br(context, value):
    _paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', '<br>\n') for p in _paragraph_re.split(escape(value)))

    if context.autoescape:
        result = Markup(result)
    return result


@blueprint.app_template_filter()
def format_date(value):
    return value.strftime('%-d %B %Y')


def format_str_as_short_date(value):
    return datetime.strptime(value, "%d/%m/%Y").strftime('%d %B %Y')


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
