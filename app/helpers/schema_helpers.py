from functools import wraps
from uuid import uuid4

from app.globals import get_session_store
from app.utilities.schema import load_schema_from_session_data


def with_schema(function):
    """Adds the survey schema as the first argument to the function being wrapped.
    Use on flask request handlers or methods called by flask request handlers.

    May error unless there is a `current_user`, so should be used as follows e.g.

    ```python
    @login_required
    @with_schema
    @full_routing_path_required
    def get_block(routing_path, schema, *args):
        ...
    ```
    """
    @wraps(function)
    def wrapped_function(*args, **kwargs):
        session_data = get_session_store().session_data
        schema = load_schema_from_session_data(session_data)
        return function(schema, *args, **kwargs)
    return wrapped_function


def get_group_instance_id(schema, answer_store, location, answer_instance=0):
    """Return a group instance_id if required, or None if not"""
    if not schema.location_requires_group_instance(location):
        return None

    dependent_drivers = schema.get_group_dependencies(location.group_id)
    if dependent_drivers:
        return _get_dependent_group_instance(schema, dependent_drivers, answer_store, location.group_instance)

    existing_answers = []
    if location.group_id in schema.get_group_dependencies_group_drivers():
        group_answer_ids = schema.get_answer_ids_for_group(location.group_id)
        existing_answers = answer_store.filter(answer_ids=group_answer_ids, group_instance=location.group_instance)

    if location.block_id in schema.get_group_dependencies_block_drivers():
        block_answer_ids = schema.get_answer_ids_for_block(location.block_id)
        existing_answers = answer_store.filter(answer_ids=block_answer_ids, answer_instance=answer_instance)

    # If there are existing answers with a group_instance_id
    if existing_answers and [x for x in existing_answers if x.get('group_instance_id')]:
        return existing_answers[0]['group_instance_id']

    return str(uuid4())


def _get_dependent_group_instance(schema, dependent_drivers, answer_store, group_instance):
    group_instance_ids = []
    for driver_id in dependent_drivers:
        if driver_id in schema.get_group_dependencies_group_drivers():
            driver_answer_ids = schema.get_answer_ids_for_group(driver_id)
            group_instance_ids.extend(_get_group_instance_ids_for_group(answer_store, driver_answer_ids))
        if driver_id in schema.get_group_dependencies_block_drivers():
            driver_answer_ids = schema.get_answer_ids_for_block(driver_id)
            group_instance_ids.extend(_get_group_instance_ids_for_block(answer_store, driver_answer_ids))

    return group_instance_ids[group_instance]


def _get_group_instance_ids_for_group(answer_store, group_answer_ids):
    group_instance_ids = []

    group_instances = 0
    for answer in list(answer_store.filter(answer_ids=group_answer_ids)):
        group_instances = max(group_instances, answer['group_instance'])

    for i in range(group_instances + 1):
        answers = list(answer_store.filter(answer_ids=group_answer_ids, group_instance=i))
        if answers:
            group_instance_ids.append(answers[0]['group_instance_id'])

    return group_instance_ids


def _get_group_instance_ids_for_block(answer_store, block_answer_ids):
    group_instance_ids = []

    answer_instances = 0
    for answer in list(answer_store.filter(answer_ids=block_answer_ids)):
        answer_instances = max(answer_instances, answer['answer_instance'])

    for i in range(answer_instances + 1):
        answers = list(answer_store.filter(answer_ids=block_answer_ids, answer_instance=i))
        if answers:
            group_instance_ids.append(answers[0]['group_instance_id'])

    return group_instance_ids
