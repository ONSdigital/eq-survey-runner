from flask import Blueprint

main_blueprint = Blueprint('main', __name__)

from app.main.views import root         # NOQA


@main_blueprint.after_request
def add_cache_control(response):
    response.cache_control.no_cache = True
    return response
