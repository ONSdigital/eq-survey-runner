from flask import g
from flask_login import current_user
from werkzeug.local import LocalProxy

from app.globals import get_answer_store, get_metadata
from app.questionnaire.path_finder import PathFinder


def get_path_finder():
    finder = getattr(g, '_path_finder', None)

    if finder is None:
        metadata = get_metadata(current_user)
        answer_store = get_answer_store(current_user)
        finder = PathFinder(g.schema_json, answer_store, metadata)

    return finder


path_finder = LocalProxy(get_path_finder)
