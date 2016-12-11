def evaluate_rule(when, answer_value):
    """
    Determine whether a rule will be satisfied based on a given answer
    :param when:
    :param answer_value:
    :return:
    """
    match_value = when['value']
    condition = when['condition']

    answer_to_test = str(answer_value)

    if isinstance(answer_value, list):
        if len(answer_value) == 1:
            answer_to_test = answer_value[0]
        else:
            return False

    # Evaluate the condition on the routing rule
    if condition == 'equals' and match_value == answer_to_test:
        return True
    elif condition == 'not equals' and match_value != answer_to_test:
        return True
    return False


def evaluate_goto(goto_rule, metadata, answer_store, group_instance):
    """
    Determine whether a goto rule will be satisfied based on a given answer
    :param goto_rule:
    :param metadata
    :param answer_store:
    :param group_instance:
    :return:
    """
    if 'when' in goto_rule.keys():

        when = goto_rule['when']

        if 'id' in when:
            answer_index = when['id']
            filtered = answer_store.filter(answer_id=answer_index, group_instance=group_instance)
            if len(filtered) == 1:
                return evaluate_rule(when, filtered[0]['value'])

        elif 'meta' in when:
            key = when['meta']
            value = get_metadata_value(metadata, key)
            return evaluate_rule(when, value)

        return False
    return True


def evaluate_repeat(repeat_rule, answer_store):
    """
    Returns the number of times repetition should occur based on answers
    :param repeat_rule:
    :param answer_store:
    :return: The number of times to repeat
    """
    repeat_functions = {
        'answer_value': lambda filtered_answers: int(filtered_answers[0]['value'] if len(filtered_answers) == 1 else 1),
        'answer_count': len,
        'answer_count_minus_one': lambda filtered_answers: len(filtered_answers) - 1,
    }
    if 'answer_id' in repeat_rule and 'type' in repeat_rule:
        repeat_index = repeat_rule['answer_id']
        filtered = answer_store.filter(answer_id=repeat_index)
        repeat_function = repeat_functions[repeat_rule['type']]
        return repeat_function(filtered)


def get_metadata_value(metadata, keys):
    if not _contains_in_dict(metadata, keys):
        return None

    if "." in keys:
        key, rest = keys.split(".", 1)
        return get_metadata_value(metadata[key], rest)
    else:
        return metadata[keys]


def _contains_in_dict(metadata, keys):
    if "." in keys:
        key, rest = keys.split(".", 1)
        if key not in metadata:
            return False
        return _contains_in_dict(metadata[key], rest)
    else:
        return keys in metadata
