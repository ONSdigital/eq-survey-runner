import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
MAX_REPEATS = 25

logger = logging.getLogger(__name__)


def evaluate_rule(when, answer_value):
    """
    Determine whether a rule will be satisfied based on a given answer
    :param when:
    :param answer_value:
    :return:
    """
    match_value = when['value'] if 'value' in when else None
    condition = when['condition']

    result = False

    # Evaluate the condition on the routing rule
    if condition == 'equals' and match_value == answer_value:
        result = True
    elif condition == 'not equals' and match_value != answer_value:
        result = True
    elif condition == 'contains' and isinstance(answer_value, list) and match_value in answer_value:
        result = True
    elif condition == 'not contains' and isinstance(answer_value, list) and match_value not in answer_value:
        result = True
    elif condition == 'not set':
        result = answer_value is None
    elif condition == 'greater than' and isinstance(answer_value, int) and answer_value > match_value:
        result = True
    elif condition == 'less than' and isinstance(answer_value, int) and answer_value < match_value:
        result = True

    return result


def evaluate_date_rule(when, answer_store, group_instance, metadata, answer_value):
    result = False

    date_comparison = when['date_comparison']

    answer_value = convert_to_datetime(answer_value)
    match_value = get_date_match_value(date_comparison, answer_store, group_instance, metadata)
    condition = when.get('condition')

    if not answer_value or not match_value or not condition:
        return False

    if condition == 'equals' and match_value == answer_value:
        result = True
    elif condition == 'not equals' and match_value != answer_value:
        result = True
    elif condition == 'greater than' and answer_value > match_value:
        result = True
    elif condition == 'less than' and answer_value < match_value:
        result = True

    return result


def get_date_match_value(date_comparison, answer_store, group_instance, metadata):
    match_value = None

    if 'value' in date_comparison:
        if date_comparison['value'] == 'now':
            match_value = datetime.utcnow().strftime('%Y-%m-%d')
        else:
            match_value = date_comparison['value']
    elif 'id' in date_comparison:
        match_value = get_answer_store_value(date_comparison['id'], answer_store, group_instance)
    elif 'meta' in date_comparison:
        match_value = get_metadata_value(metadata, date_comparison['meta'])

    match_value = convert_to_datetime(match_value)

    if 'offset_by' in date_comparison and match_value:
        offset = date_comparison['offset_by']
        match_value = match_value + relativedelta(days=offset.get('days', 0),
                                                  months=offset.get('months', 0),
                                                  years=offset.get('years', 0))

    return match_value


def convert_to_datetime(value):
    date_format = '%Y-%m-%d'
    if value and len(value) == 7:
        date_format = '%Y-%m'

    return datetime.strptime(value, date_format) if value else None


def evaluate_goto(goto_rule, metadata, answer_store, group_instance):
    """
    Determine whether a goto rule will be satisfied based on a given answer
    :param goto_rule: goto rule to evaluate
    :param metadata: metadata for evaluating rules with metadata conditions
    :param answer_store: store of answers to evaluate
    :param group_instance: when evaluating a when rule for a repeating group, defaults to 0 for non-repeating groups
    :return: True if the when condition has been met otherwise False
    """
    if 'when' in goto_rule.keys():
        return evaluate_when_rules(goto_rule['when'], metadata, answer_store, group_instance)
    return True


def evaluate_repeat(repeat_rule, answer_store, answer_ids_on_path):
    """
    Returns the number of times repetition should occur based on answers
    :param repeat_rule:
    :param answer_store:
    :param max_repeats:
    :return: The number of times to repeat
    """
    repeat_functions = {
        'answer_value': _get_answer_value,
        'answer_count': len,
        'answer_count_minus_one': lambda f: min(_get_answer_count(f), MAX_REPEATS - 1),
    }
    if 'answer_id' in repeat_rule and 'type' in repeat_rule:
        repeat_index = repeat_rule['answer_id']

        answers = []
        # Only use answers that are on the routing path
        if repeat_index in answer_ids_on_path:
            answers = list(answer_store.filter(answer_ids=[repeat_index]))

        repeat_function = repeat_functions[repeat_rule['type']]
        no_of_repeats = repeat_function(answers)

        if no_of_repeats > MAX_REPEATS:
            logger.warning('Excessive number of repeats found [%s] capping at [%s]', no_of_repeats, MAX_REPEATS)
            no_of_repeats = MAX_REPEATS

        return no_of_repeats


def _get_answer_value(filtered_answers):
    return int(filtered_answers[0]['value'] if len(filtered_answers) == 1 and filtered_answers[0]['value'] else 0)


def _get_answer_count(filtered_answers):
    return len(filtered_answers) - 1 if len(filtered_answers) > 0 else 0  # pylint: disable=len-as-condition


def evaluate_skip_conditions(skip_conditions, metadata, answer_store, group_instance=0):
    """
    Determine whether a skip condition will be satisfied based on a given answer
    :param skip_conditions: skip_conditions rule to evaluate
    :param metadata: metadata for evaluating rules with metadata conditions
    :param answer_store: store of answers to evaluate
    :param group_instance: when evaluating a when rule for a repeating group, defaults to 0 for non-repeating groups
    :return: True if the when condition has been met otherwise False
    """

    no_skip_condition = skip_conditions is None or len(skip_conditions) == 0
    if no_skip_condition:
        return False

    for when in skip_conditions:
        condition = evaluate_when_rules(when['when'], metadata, answer_store, group_instance)
        if condition is True:
            return True
    return False


def evaluate_when_rules(when_rules, metadata, answer_store, group_instance):
    """
    Whether the skip condition has been met.
    :param when_rules: when rules to evaluate
    :param metadata: metadata for evaluating rules with metadata conditions
    :param answer_store: store of answers to evaluate
    :param group_instance: when evaluating a when rule for a repeating group
    :return: True if the when condition has been met otherwise False
    """
    for when_rule in when_rules:
        if 'id' in when_rule:
            value = get_answer_store_value(when_rule['id'], answer_store, group_instance)
        elif 'meta' in when_rule:
            value = get_metadata_value(metadata, when_rule['meta'])
        else:
            return True

        if 'date_comparison' in when_rule:
            if not evaluate_date_rule(when_rule, answer_store, group_instance, metadata, value):
                return False
        else:
            if not evaluate_rule(when_rule, value):
                return False

    return True


def get_answer_store_value(answer_index, answer_store, group_instance):
    filtered = answer_store.filter(answer_ids=[answer_index], group_instance=group_instance)

    if filtered.count() > 1:
        raise Exception('Multiple answers ({:d}) found evaluating when rule for answer ({})'
                        .format(filtered.count(), answer_index))
    return filtered[0]['value'] if filtered.count() == 1 else None


def get_metadata_value(metadata, keys):
    if not _contains_in_dict(metadata, keys):
        return None

    if '.' in keys:
        key, rest = keys.split('.', 1)
        return get_metadata_value(metadata[key], rest)
    return metadata[keys]


def is_goto_rule(rule):
    return any(key in rule.get('goto', {}) for key in ('when', 'block', 'group'))


def _contains_in_dict(metadata, keys):
    if '.' in keys:
        key, rest = keys.split('.', 1)
        if key not in metadata:
            return False
        return _contains_in_dict(metadata[key], rest)

    return keys in metadata
