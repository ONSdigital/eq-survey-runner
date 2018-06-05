from jinja2 import escape

from flask import g


def build_schema_context(metadata, answer_store, answer_ids_on_path, group_instance=0):
    """
    Build questionnaire schema context containing exercise and answers
    :param metadata: user metadata
    :param answer_store: all the answers for the given questionnaire
    :param answer_ids_on_path: a list of the answer ids on the routing path
    :param group_instance: The group instance Id passed into the url route
    :return: questionnaire schema context
    """
    return {
        'metadata': build_schema_metadata(metadata),
        'answers': _build_answers(answer_store, answer_ids_on_path),
        'group_instance': group_instance,
    }


def _build_answers(answer_store, answer_ids_on_path):
    answers = {}

    for answer_id in answer_ids_on_path:
        is_repeating_answer = _get_is_repeating_answer(answer_id)
        answer_is_in_repeating_group = _get_answer_is_in_repeating_group(answer_id)

        matching_answers = answer_store.filter(
            answer_ids=[answer_id], limit=True)

        if is_repeating_answer:
            value = _create_answers_list(matching_answers, 'answer_instance')

        elif answer_is_in_repeating_group:
            value = _create_answers_list(matching_answers, 'group_instance')

        elif matching_answers:
            value = json_and_html_safe(matching_answers[0]['value'])
        else:
            value = ''

        answers[answer_id] = value

    return answers


def build_schema_metadata(metadata):

    schema_metadata = g.schema.json['metadata']
    parsed = {key: json_and_html_safe(metadata[key]) for key in schema_metadata.keys() if key in metadata}
    trad_as = json_and_html_safe(metadata.get('trad_as'))
    ru_name = json_and_html_safe(metadata.get('ru_name'))

    if trad_as:
        parsed['trad_as'] = trad_as

    if 'trad_as_or_ru_name' in schema_metadata:
        parsed['trad_as_or_ru_name'] = trad_as or ru_name

    return parsed


def json_and_html_safe(data):
    if data and isinstance(data, str):
        return escape(data.replace('\\', r'\\'))
    return data


def _get_is_repeating_answer(answer_id):
    return g.schema.is_repeating_answer_type(answer_id)


def _get_answer_is_in_repeating_group(answer_id):
    return g.schema.answer_is_in_repeating_group(answer_id)


def _create_answers_list(answers, index_key):
    """Creates a list of repeating answer values in the same index position
    as that specified by their `group_instance` or `answer_instance`

    Example:

    answers = [{
        'value': 'foo',
        'group_instance': 2,
        'answer_instance': 0,
        'answer_id': 'bar'}]

    answer_values = _create_answers_list(answers, 'group_instance')

    answer_values will be ['', '', 'foo']

    :param answers: list of answer dicts
    :param index_key: key of index value. 'group_instance' or 'answer_instance'
    :return: List of values. Empty values are padded.
    """
    items = []
    for answer in answers:
        index = answer[index_key]
        if len(items) < index:
            items.extend([''] * index)

        value = json_and_html_safe(answer['value'])
        if len(items) == index:
            items.append(value)
        else:
            items[index] = value

    return items
