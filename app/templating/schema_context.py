from app.utilities.date_utils import to_date


def build_schema_context(metadata, aliases, answers):
    """
    Build questionnaire schema context containing exercise and answers
    :param metadata: user metadata
    :param aliases: alias mapping of friendly names to answer ids
    :param answers: all the answers for the given questionnaire
    :return: questionnaire schema context
    """
    return {
        "exercise": _build_exercise(metadata),
        "answers": _map_alias_to_answers(aliases, answers),
    }


def _map_alias_to_answers(aliases, answers):
    values = {}
    for alias, item_id in aliases.items():
        value = answers.get(item_id)
        values[alias] = value if value else ""
    return values


def _build_exercise(metadata):
    return {
        "start_date": to_date(metadata["ref_p_start_date"]),
        "end_date": to_date(metadata["ref_p_end_date"]),
        "employment_date": to_date(metadata["employment_date"]),
        "return_by": to_date(metadata["return_by"]),
        "region_code": metadata["region_code"],
    }
