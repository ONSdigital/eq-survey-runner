from flask import g
from flask_login import current_user, login_required
from werkzeug.local import LocalProxy

from app.globals import (
    get_answer_store,
    get_metadata,
    get_progress_store,
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
        progress_store = get_progress_store(current_user)
        list_store = get_list_store(current_user)
        finder = PathFinder(
            g.schema, answer_store, metadata, progress_store, list_store
        )
        g.path_finder = finder
    return finder


path_finder = LocalProxy(get_path_finder)
