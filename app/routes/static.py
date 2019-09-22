from flask import Blueprint
from structlog import get_logger

from app.helpers.language_helper import handle_language
from app.helpers.template_helper import render_template

logger = get_logger()

static_blueprint = Blueprint(name='static', import_name=__name__)


@static_blueprint.before_request
def before_static_request():
    handle_language()


@static_blueprint.route('/privacy', methods=['GET'])
def privacy():
    return render_template('static/privacy')


@static_blueprint.route('/accessibility', methods=['GET'])
def accessibility():
    return render_template('static/accessibility')
