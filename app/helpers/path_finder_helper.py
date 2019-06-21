from functools import wraps

from flask import g
from flask_login import current_user, login_required
from werkzeug.local import LocalProxy

from app.globals import (
    get_answer_store,
    get_metadata,
    get_completed_store,
    get_list_store,
)
from app.questionnaire.path_finder import PathFinder


@login_required
def get_path_finder():
    try:
        finder = g.path_finder
    except AttributeError:
        metadata = get_metadata(current_user)
        answer_store = get_answer_store(current_user)
        completed_store = get_completed_store(current_user)
        list_store = get_list_store(current_user)
        finder = PathFinder(
            g.schema, answer_store, metadata, completed_store, list_store
        )
        g.path_finder = finder
    return finder


path_finder = LocalProxy(get_path_finder)


def section_routing_path_required(function):
    @wraps(function)
    def wrap_function(*args, **kwargs):
        block_id = kwargs['block_id']
        block = g.schema.get_block(block_id)

        if not block:
            return function(None, *args, **kwargs)

        section = g.schema.get_section_for_block_id(block_id)
        routing_path = path_finder.routing_path(section)
        return function(routing_path, *args, **kwargs)

    return wrap_function
