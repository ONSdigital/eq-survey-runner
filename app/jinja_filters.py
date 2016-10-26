import re

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
def pretty_date(value):
    return value.strftime('%-d %B %Y')


def pretty_short_date(value):
    return value.strftime('%d %b %Y')


@blueprint.app_template_filter()
def pretty_date_range(value):
    from_date = pretty_short_date(value['from'])
    to_date = pretty_short_date(value['to'])
    return '{from_date} to {to_date}'.format(from_date=from_date, to_date=to_date)
