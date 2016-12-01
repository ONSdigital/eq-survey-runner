from app.utilities.date_utils import to_date


def build_schema_context(metadata, aliases, answer_store, group_instance=0):
    """
    Build questionnaire schema context containing exercise and answers
    :param metadata: user metadata
    :param aliases: alias mapping of friendly names to answer ids
    :param answer_store: all the answers for the given questionnaire
    :param group_instance: The group instance Id passed into the url route
    :return: questionnaire schema context
    """
    return {
        "exercise": _build_exercise(metadata),
        "answers": _map_alias_to_answers(aliases, answer_store),
        "group_instance": group_instance,
    }


def _map_alias_to_answers(aliases, answer_store):
    values = {}
    for alias, answer_info in aliases.items():
        matching_answers = []

        answers = answer_store.filter(answer_id=answer_info['answer_id'])
        matching_answers.extend([answer['value'] for answer in answers])

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
        "start_date": to_date(metadata["ref_p_start_date"]),
        "end_date": to_date(metadata["ref_p_end_date"]),
        "employment_date": to_date(metadata["employment_date"]),
        "return_by": to_date(metadata["return_by"]),
        "region_code": metadata["region_code"],
    }
