from functools import wraps

from flask import g
from flask_login import current_user, login_required

from app.globals import get_answer_store_async, get_metadata_async, get_completed_blocks_async
from app.questionnaire.path_finder import PathFinder


@login_required
async def get_path_finder():
    finder = getattr(g, 'path_finder', None)

    if finder is None:
        metadata = await get_metadata_async(current_user)
        answer_store = await get_answer_store_async(current_user)
        completed_blocks = await get_completed_blocks_async(current_user)
        finder = PathFinder(g.schema, answer_store, metadata, completed_blocks)
        g.path_finder = finder

    return finder


def full_routing_path_required(function):
    @wraps(function)
    async def wrap_function(*args, **kwargs):
        routing_path = (await get_path_finder()).get_full_routing_path()
        return await function(routing_path, *args, **kwargs)
    return wrap_function
