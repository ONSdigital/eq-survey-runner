from bs4 import BeautifulSoup

import flask

import jinja2

blueprint = flask.Blueprint('filters', __name__)


@jinja2.contextfilter
@blueprint.app_template_filter()
def strcat(context, mylist, mystr):
    return [mystr + s for s in mylist]

blueprint.add_app_template_filter(strcat)


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


@jinja2.contextfilter
@blueprint.app_template_filter()
def merge(context, target_obj, dict_args):
    for property in dict_args.keys():
        setattr(target_obj, property, dict_args[property])
    return target_obj


blueprint.add_app_template_filter(merge)


@jinja2.contextfilter
@blueprint.app_template_filter()
def print_type(context, value):
    return type(value)

blueprint.add_app_template_filter(print_type)
