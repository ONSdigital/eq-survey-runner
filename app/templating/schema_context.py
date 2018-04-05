from jinja2 import escape


def build_schema_context(metadata, aliases, answer_store, answer_ids_on_path, group_instance=0):
    """
    Build questionnaire schema context containing exercise and answers
    :param metadata: user metadata
    :param aliases: alias mapping of friendly names to answer ids
    :param answer_store: all the answers for the given questionnaire
    :param answer_ids_on_path: a list of the answer ids on the routing path
    :param group_instance: The group instance Id passed into the url route
    :return: questionnaire schema context
    """
    return {
        'exercise': _build_exercise(metadata),
        'respondent': _build_respondent(metadata),
        'answers': _map_alias_to_answers(aliases, answer_store, answer_ids_on_path),
        'group_instance': group_instance,
    }


def _map_alias_to_answers(aliases, answer_store, answer_ids_on_path):
    values = {}
    for alias, answer_info in aliases.items():
        matching_answers = []

        answers = answer_store.filter(answer_ids=[answer_info['answer_id']], limit=True)

        for answer in answers:
            if answer['answer_id'] in answer_ids_on_path:
                safe_answer = json_and_html_safe(answer['value'])
                matching_answers.append(safe_answer)

        number_of_matches = len(matching_answers)

        if number_of_matches >= 1 and answer_info['repeats']:
            values[alias] = matching_answers
        elif number_of_matches == 1 and not answer_info['repeats']:
            values[alias] = matching_answers[0]
        else:
            values[alias] = ''

    return values


def _build_exercise(metadata):
    return {
        'start_date': metadata['ref_p_start_date'],
        'end_date': metadata.get('ref_p_end_date'),
        'period_str': json_and_html_safe(metadata.get('period_str')),
        'employment_date': metadata.get('employment_date'),
        'return_by': metadata.get('return_by'),
        'region_code': json_and_html_safe(metadata.get('region_code')),
    }


def _build_respondent(metadata):
    return {
        'ru_name': json_and_html_safe(metadata.get('ru_name')),
        'trad_as': json_and_html_safe(metadata.get('trad_as')),
        'trad_as_or_ru_name': json_and_html_safe(metadata.get('trad_as') or metadata.get('ru_name')),
    }


def json_and_html_safe(data):
    if data and isinstance(data, str):
        return escape(data.replace('\\', r'\\'))
    return data
