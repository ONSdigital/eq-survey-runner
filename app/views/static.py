from flask import Blueprint
from flask_themes2 import render_theme_template

from app.helpers import template_helper


from structlog import get_logger

logger = get_logger()

contact_blueprint = Blueprint('contact', __name__,)


@contact_blueprint.route('/contact-us', methods=['GET'])
def contact():
    return render_theme_template('default', 'static/contact-us.html')


@contact_blueprint.route('/cookies-privacy', methods=['GET'])
def legal():
    return render_theme_template('default', 'static/cookies-privacy.html')


def _render_template(template, **kwargs):
    return template_helper.render_template(template, **kwargs)
