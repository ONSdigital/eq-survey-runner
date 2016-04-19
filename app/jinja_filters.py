from bs4 import BeautifulSoup
import jinja2
import flask

blueprint = flask.Blueprint('filters', __name__)


@jinja2.contextfilter
@blueprint.app_template_filter()
def format_currency(context, value):
    return "£{:,}".format(value)

blueprint.add_app_template_filter(format_currency)


@jinja2.contextfilter
@blueprint.app_template_filter()
def prettify(context, code):
    soup = BeautifulSoup(code)
    return soup.html.body.contents[0].prettify()

blueprint.add_app_template_filter(prettify)


@jinja2.contextfilter
@blueprint.app_template_filter()
def dumpobj(context, my_obj):
    if isinstance(my_obj, str) or isinstance(my_obj, int):
        return my_obj

    variables = vars(my_obj)
    output = {}
    for key, value in variables.items():
        if key == 'container':
            output[key] = value
        elif isinstance(value, str) or isinstance(value, int):
            output[key] = value
        elif '__dict__' in dir(value):
            output[key] = dumpobj(None, value)
        elif '__iter__' in dir(value):
            output[key] = []
            for item in value:
                output[key].append(dumpobj(None, item))
    return output

blueprint.add_app_template_filter(dumpobj)
