from bs4 import BeautifulSoup
import jinja2
import flask

blueprint = flask.Blueprint('filters', __name__)


@jinja2.contextfilter
@blueprint.app_template_filter()
def prettify(context, code):
    soup = BeautifulSoup(code)
    return soup.prettify()

blueprint.add_app_template_filter(prettify)


@jinja2.contextfilter
@blueprint.app_template_filter()
def dumpobj(context, my_obj):
    return vars(my_obj)

blueprint.add_app_template_filter(dumpobj)
