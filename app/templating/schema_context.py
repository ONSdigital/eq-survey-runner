from jinja2 import escape

from app.questionnaire.location import Location
from app.utilities.date_utils import to_date


def build_schema_context(metadata, aliases, answer_store, routing_path, group_instance=0):
    """
    Build questionnaire schema context containing exercise and answers
    :param metadata: user metadata
    :param aliases: alias mapping of friendly names to answer ids
    :param answer_store: all the answers for the given questionnaire
    :param routing_path:
    :param group_instance: The group instance Id passed into the url route
    :return: questionnaire schema context
    """
    return {
        "exercise": _build_exercise(metadata),
        "respondent": _build_respondent(metadata),
        "answers": _map_alias_to_answers(aliases, answer_store, routing_path),
        "group_instance": group_instance,
    }


def _map_alias_to_answers(aliases, answer_store, routing_path):
    values = {}
    for alias, answer_info in aliases.items():
        matching_answers = []

        answers = answer_store.filter(answer_id=answer_info['answer_id'], limit=True)

        for answer in answers:
            if _is_answer_in_routing_path(routing_path, answer):
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


def _is_answer_in_routing_path(routing_path, answer):
    location = Location(answer['group_id'], answer['group_instance'], answer['block_id'])

    return location in routing_path


def _build_exercise(metadata):
    return {
        "start_date": to_date(metadata["ref_p_start_date"]),
        "end_date": to_date(metadata["ref_p_end_date"]),
        "period_str": json_and_html_safe(metadata["period_str"]),
        "employment_date": to_date(metadata["employment_date"]),
        "return_by": to_date(metadata["return_by"]),
        "region_code": json_and_html_safe(metadata["region_code"]),
    }


def _build_respondent(metadata):
    return {
        "ru_name": json_and_html_safe(metadata["ru_name"]),
        "trad_as": json_and_html_safe(metadata["trad_as"]),
        "trad_as_or_ru_name": json_and_html_safe(metadata["trad_as"] or metadata["ru_name"]),
    }


def json_and_html_safe(data):
    if isinstance(data, str):
        return escape(data.replace('\\', r'\\'))
    else:
        return data
