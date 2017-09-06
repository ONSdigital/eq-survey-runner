from functools import wraps

from flask import g
from flask_login import current_user
from werkzeug.local import LocalProxy

from app.globals import get_answer_store, get_metadata
from app.questionnaire.path_finder import PathFinder


def get_path_finder():
    finder = getattr(g, 'path_finder', None)

    if finder is None:
        metadata = get_metadata(current_user)
        answer_store = get_answer_store(current_user)
        finder = PathFinder(g.schema_json, answer_store, metadata)
        g.path_finder = finder

    return finder


path_finder = LocalProxy(get_path_finder)


def full_routing_path_required(function):
    @wraps(function)
    def wrap_function(*args, **kwargs):
        routing_path = path_finder.get_full_routing_path()
        return function(routing_path, *args, **kwargs)
    return wrap_function
