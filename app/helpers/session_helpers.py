from functools import wraps

from flask_login import current_user

from app.globals import get_answer_store, get_metadata, get_collection_metadata


def with_answer_store(function):
    """Adds the `answer_store` as an argument, where the `current_user` is defined.
    Use on flask request handlers or methods called by flask request handlers.

    May error unless there is a `current_user`."""
    @wraps(function)
    def wrapped_function(*args, **kwargs):
        answer_store = get_answer_store(current_user)
        return function(answer_store, *args, **kwargs)
    return wrapped_function


def with_metadata(function):
    """Adds `metadata` as an argument, where the `current_user` is defined.
    Use on flask request handlers or methods called by flask request handlers.

    May error unless there is a `current_user`."""
    @wraps(function)
    def other_wrapped_function(*args, **kwargs):
        metadata = get_metadata(current_user)
        return function(metadata, *args, **kwargs)
    return other_wrapped_function


def with_collection_metadata(function):
    """Adds `collection_metadata` as an argument, where the `current_user` is defined.
    Use on flask request handlers or methods called by flask request handlers.

    May error unless there is a `current_user`."""
    @wraps(function)
    def other_wrapped_function(*args, **kwargs):
        collection_metadata = get_collection_metadata(current_user)
        return function(collection_metadata, *args, **kwargs)
    return other_wrapped_function
