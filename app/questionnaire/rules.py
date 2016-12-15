def evaluate_rule(when, answer_value):
    """
    Determine whether a rule will be satisfied based on a given answer
    :param when:
    :param answer_value:
    :return:
    """
    match_value = when['value']
    condition = when['condition']

    answer_to_test = str(answer_value) if condition in ['equals', 'not equals'] and not isinstance(answer_value, bool) else answer_value

    # Evaluate the condition on the routing rule
    if condition == 'equals' and match_value == answer_to_test:
        return True
    elif condition == 'not equals' and match_value != answer_to_test:
        return True
    elif condition == 'contains' and isinstance(answer_to_test, list) and match_value in answer_to_test:
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
        for when_rule in goto_rule['when']:
            if 'id' in when_rule:
                answer_index = when_rule['id']
                filtered = answer_store.filter(answer_id=answer_index, group_instance=group_instance)

                assert len(filtered) <= 1, "Condition will not met: Multiple ({:d}) answers found".format(len(filtered))

                if len(filtered) == 1 and not evaluate_rule(when_rule, filtered[0]['value']):
                    return False
                elif len(filtered) == 0:
                    return False

            elif 'meta' in when_rule:
                key = when_rule['meta']
                value = get_metadata_value(metadata, key)
                if not evaluate_rule(when_rule, value):
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
        'answer_value': lambda filtered_answers: int(filtered_answers[0]['value'] if len(filtered_answers) == 1 else 0),
        'answer_count': len,
        'answer_count_minus_one': lambda filtered_answers: len(filtered_answers) - 1 if len(filtered_answers) > 0 else 0,
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


def is_goto_rule(rule):
    return 'goto' in rule and 'when' in rule['goto'].keys() or 'id' in rule['goto'].keys()


def _contains_in_dict(metadata, keys):
    if "." in keys:
        key, rest = keys.split(".", 1)
        if key not in metadata:
            return False
        return _contains_in_dict(metadata[key], rest)
    else:
        return keys in metadata
