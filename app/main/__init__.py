from flask import Blueprint

main = Blueprint('main', __name__)

from app.main.views import root         # NOQA


@main.after_request
def add_cache_control(response):
    response.cache_control.no_cache = True
    return response
