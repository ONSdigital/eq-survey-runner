from flask import Blueprint

patternlib_blueprint = Blueprint('patternlib', __name__, template_folder='templates')

from . import views  # NOQA
