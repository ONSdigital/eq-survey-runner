from functools import wraps

from flask_login import current_user

from app.globals import get_answer_store_async, get_metadata_async, get_collection_metadata_async


def with_answer_store(function):
    """Adds the `answer_store` as an argument, where the `current_user` is defined.
    Use on flask request handlers or methods called by flask request handlers.

    May error unless there is a `current_user`."""
    @wraps(function)
    async def wrapped_function(*args, **kwargs):
        answer_store = await get_answer_store_async(current_user)
        return await function(answer_store, *args, **kwargs)
    return wrapped_function


def with_metadata(function):
    """Adds `metadata` as an argument, where the `current_user` is defined.
    Use on flask request handlers or methods called by flask request handlers.

    May error unless there is a `current_user`."""
    @wraps(function)
    async def other_wrapped_function(*args, **kwargs):
        metadata = await get_metadata_async(current_user)
        return await function(metadata, *args, **kwargs)
    return other_wrapped_function


def with_collection_metadata(function):
    """Adds `collection_metadata` as an argument, where the `current_user` is defined.
    Use on flask request handlers or methods called by flask request handlers.

    May error unless there is a `current_user`."""
    @wraps(function)
    async def other_wrapped_function(*args, **kwargs):
        collection_metadata = await get_collection_metadata_async(current_user)
        return await function(collection_metadata, *args, **kwargs)
    return other_wrapped_function
