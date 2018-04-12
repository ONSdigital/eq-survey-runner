from functools import wraps

from flask import g
from flask_login import current_user, login_required
from werkzeug.local import LocalProxy

from app.globals import get_answer_store, get_metadata, get_completed_blocks
from app.questionnaire.path_finder import PathFinder


@login_required
def get_path_finder():
    finder = getattr(g, 'path_finder', None)

    if finder is None:
        metadata = get_metadata(current_user)
        answer_store = get_answer_store(current_user)
        completed_blocks = get_completed_blocks(current_user)
        finder = PathFinder(g.schema, answer_store, metadata, completed_blocks)
        g.path_finder = finder

    return finder


path_finder = LocalProxy(get_path_finder)


def full_routing_path_required(function):
    @wraps(function)
    def wrap_function(*args, **kwargs):
        routing_path = path_finder.get_full_routing_path()
        return function(routing_path, *args, **kwargs)
    return wrap_function
