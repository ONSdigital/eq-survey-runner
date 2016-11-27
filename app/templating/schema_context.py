from flask import request

from app.utilities.date_utils import to_date
from app.questionnaire_state.state_repeating_answer_question import iterate_over_instance_ids



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
        "current": request.view_args,
    }


def _map_alias_to_answers(aliases, answers):
    values = {}
    for alias, item_id in aliases.items():
        matching_answers = []
        for answer_id, answer_index in iterate_over_instance_ids(answers):
            if answer_id == item_id:
                key = '_'.join([answer_id, str(answer_index)]) if answer_index > 0 else answer_id
                matching_answers.append(answers.get(key))

        number_of_matches = len(matching_answers)

        if number_of_matches > 1:
            values[alias] = matching_answers
        elif number_of_matches == 1:
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
