from flask import Blueprint

dev_mode_blueprint = Blueprint('dev_mode', __name__, template_folder='templates')

from . import views  # NOQA
