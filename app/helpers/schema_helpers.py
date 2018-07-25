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


def get_group_instance_id(schema, answer_store, location):
    repeat_rule = _get_group_repeat_rule(schema, location)
    if repeat_rule:
        group_instance_ids = []
        for group_id in repeat_rule['group_ids']:
            group_answer_ids = schema.get_answer_ids_for_group(group_id)
            group_instance_ids += _get_group_instance_ids(answer_store, group_answer_ids)

        return group_instance_ids[location.group_instance]

    group_answer_ids = schema.get_answer_ids_for_group(location.group_id)
    existing_answers = answer_store.filter(answer_ids=group_answer_ids, group_instance=location.group_instance)
    if existing_answers:
        return existing_answers[0]['group_instance_id']

    return '-'.join([location.group_id, str(uuid4())])


def _get_group_repeat_rule(schema, location):
    group = schema.get_group(location.group_id)

    for routing_rule in group.get('routing_rules', []):
        if 'repeat' in routing_rule:
            repeat_rule = routing_rule['repeat']
            if repeat_rule['type'] == 'group':
                return repeat_rule


def _get_group_instance_ids(answer_store, group_answer_ids):
    group_instance_ids = []

    group_instances = 0
    for answer in list(answer_store.filter(answer_ids=group_answer_ids)):
        group_instances = max(group_instances, answer['group_instance'])

    for i in range(group_instances + 1):
        answers = list(answer_store.filter(answer_ids=group_answer_ids, group_instance=i))
        if answers:
            group_instance_ids.append(answers[0]['group_instance_id'])

    return group_instance_ids
