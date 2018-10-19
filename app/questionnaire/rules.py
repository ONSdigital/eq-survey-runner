import logging
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta

from app.questionnaire.location import Location
from app.data_model.answer_store import AnswerStore

MAX_REPEATS = 25

logger = logging.getLogger(__name__)


def evaluate_comparison_rule(when, answer_value, comparison_value):
    """
    Determine whether a comparison rule will be satisfied based on an
    answer value, and a value to compare it to.
    :param when: The when clause to evaluate
    :param answer_value: The value of the answer
    :param comparison_value: The value to compare the answer to.
    :return (bool): The result of the evaluation
    """
    condition = when['condition']

    return evaluate_condition(condition, answer_value, comparison_value)


def evaluate_rule(when, answer_value):
    """
    Determine whether a rule will be satisfied based on a given answer
    :param when: The when clause to evaluate
    :param answer_value: The value of the answer
    :return (bool): The result of the evaluation
    """

    match_value = when['value'] if 'value' in when else None

    condition = when['condition']

    # Evaluate the condition on the routing rule
    return evaluate_condition(condition, answer_value, match_value)


def evaluate_date_rule(when, answer_store, schema, group_instance, metadata, answer_value):
    date_comparison = when['date_comparison']

    answer_value = convert_to_datetime(answer_value)
    match_value = get_date_match_value(date_comparison, answer_store, schema, group_instance, metadata)
    condition = when.get('condition')

    if not answer_value or not match_value or not condition:
        return False

    # Evaluate the condition on the routing rule
    return evaluate_condition(condition, answer_value, match_value)


def evaluate_condition(condition, answer_value, match_value):
    """
    :param condition: string representation of comparison operator
    :param answer_value: the left hand operand in the comparison
    :param match_value: the right hand operand in the comparison
    :return: value of comparing lhs and rhs using the specified operator
    """
    result = False
    answer_and_match = answer_value is not None and match_value is not None

    if condition == 'equals' and answer_value == match_value:
        result = True
    elif condition == 'not equals' and answer_value != match_value:
        result = True
    elif condition == 'contains' and isinstance(answer_value, list) and match_value in answer_value:
        result = True
    elif condition == 'not contains' and isinstance(answer_value, list) and match_value not in answer_value:
        result = True
    elif condition == 'set':
        result = answer_value is not None and answer_value != []
    elif condition == 'not set':
        result = answer_value is None or answer_value == []
    elif condition == 'greater than' and answer_and_match and answer_value > match_value:
        result = True
    elif condition == 'less than' and answer_and_match and answer_value < match_value:
        result = True

    return result


def get_date_match_value(date_comparison, answer_store, schema, group_instance, metadata):
    match_value = None

    if 'value' in date_comparison:
        if date_comparison['value'] == 'now':
            match_value = datetime.utcnow().strftime('%Y-%m-%d')
        else:
            match_value = date_comparison['value']
    elif 'id' in date_comparison:
        match_value = get_answer_store_value(date_comparison['id'], answer_store, schema, group_instance)
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
    date_format = '%Y-%m'
    if value and re.match(r'\d{4}-\d{2}-\d{2}', value):
        date_format = '%Y-%m-%d'
    if value and re.match(r'\d{4}$', value):
        date_format = '%Y'

    return datetime.strptime(value, date_format) if value else None


def evaluate_goto(goto_rule, schema, metadata, answer_store, group_instance, group_instance_id=None, routing_path=None):
    """
    Determine whether a goto rule will be satisfied based on a given answer
    :param goto_rule: goto rule to evaluate
    :param schema: survey schema
    :param metadata: metadata for evaluating rules with metadata conditions
    :param answer_store: store of answers to evaluate
    :param group_instance: when evaluating a when rule for a repeating group, defaults to 0 for non-repeating groups
    :param group_instance_id: The group instance ID to filter results by
    :return: True if the when condition has been met otherwise False
    """
    if 'when' in goto_rule:
        return evaluate_when_rules(
            goto_rule['when'],
            schema,
            metadata,
            answer_store,
            group_instance,
            group_instance_id=group_instance_id,
            routing_path=routing_path,
        )
    return True


def evaluate_repeat(repeat_rule, answer_store, schema, routing_path):
    """
    Returns the number of times repetition should occur based on answers
    """
    if repeat_rule['type'] == 'until':
        when = repeat_rule['when']
        when_ids = [rule['id'] for rule in when]

        answers = list(answer_store.filter(answer_ids=when_ids))

        no_of_repeats = 1

        for answer in answers:
            group_instance = answer['group_instance']
            if evaluate_when_rules(when, schema, {}, answer_store, group_instance,
                                   group_instance_id=(answer['group_instance_id'] or None)):
                break

            no_of_repeats = no_of_repeats + 1
    else:
        repeat_functions = {
            'answer_value': _get_answer_value,
            'answer_count': len,
            'answer_count_minus_one': _get_answer_count_minus_one,
        }

        answers = _get_answers_on_routing_path_with_repeats(schema, routing_path, answer_store, repeat_rule)

        repeat_function = repeat_functions[repeat_rule['type']]
        no_of_repeats = repeat_function(answers)

    if no_of_repeats > MAX_REPEATS:
        logger.warning('Excessive number of repeats found [%s] capping at [%s]', no_of_repeats, MAX_REPEATS)
        no_of_repeats = MAX_REPEATS

    return no_of_repeats


def _get_answers_on_routing_path_with_repeats(schema, routing_path, answer_store, repeat_rule):
    repeat_indexes = []

    answer_ids_on_path = get_answer_ids_on_routing_path(
        schema, routing_path)

    # Only use answers that are on the routing path
    if 'answer_id' in repeat_rule and repeat_rule['answer_id'] in answer_ids_on_path:
        repeat_indexes.append(repeat_rule['answer_id'])

    if 'answer_ids' in repeat_rule:
        for answer_id in repeat_rule['answer_ids']:
            # Only use answers that are on the routing path
            if answer_id in answer_ids_on_path:
                repeat_indexes.append(answer_id)

    answers = answer_store.filter(answer_ids=repeat_indexes)

    # Exclude answers that are not on the routing path from repeat function
    answers_on_path = _get_answers_on_path(answers, schema, routing_path)

    return answers_on_path


def _get_answers_on_path(answers, schema, routing_path) -> AnswerStore:
    """
    Get any answers that are on the routing path and return an answer store.
    """
    answers_to_remove = [answer for answer in answers if not _is_answer_on_path(schema, answer, routing_path)]

    answers_on_path = answers.copy()

    for answer in answers_to_remove:
        answers_on_path.answers.remove(answer)

    return answers_on_path


def _is_answer_on_path(schema, answer, routing_path):
    answer_schema = schema.get_answer(answer['answer_id'])
    question_schema = schema.get_question(answer_schema['parent_id'])
    block_schema = schema.get_block(question_schema['parent_id'])
    location = Location(block_schema['parent_id'], answer['group_instance'], block_schema['id'])
    return location in routing_path


def _get_answer_value(filtered_answers):
    return int(filtered_answers[0]['value'] if len(filtered_answers) == 1 and filtered_answers[0]['value'] else 0)


def _get_answer_count_minus_one(filtered_answers):
    return min(max(len(filtered_answers) - 1, 0), MAX_REPEATS - 1)


def _get_comparison_id_value(when_rule, answer_store, schema, group_instance, group_instance_id):
    """
        Gets the value of an answer specified as an operand in a comparator ( i.e right hand argument ,
        or rhs in if lhs>rhs ) In a when clause
        If the comparison answer is not in a repeating group, we may have the wrong group_instance
        If it has a group_instance_id, we should match the group_instance_id to the current one.
    """
    answer_id = when_rule['comparison_id']

    return get_answer_store_value(answer_id, answer_store, schema, group_instance=group_instance, group_instance_id=group_instance_id)


def evaluate_skip_conditions(skip_conditions, schema, metadata, answer_store, group_instance=0, group_instance_id=None, routing_path=None):
    """
    Determine whether a skip condition will be satisfied based on a given answer
    :param skip_conditions: skip_conditions rule to evaluate
    :param schema: survey schema
    :param metadata: metadata for evaluating rules with metadata conditions
    :param answer_store: store of answers to evaluate
    :param group_instance: when evaluating a when rule for a repeating group, defaults to 0 for non-repeating groups
    :param group_instance_id: The group instance ID to filter results by
    :return: True if the when condition has been met otherwise False
    """

    no_skip_condition = skip_conditions is None or len(skip_conditions) == 0
    if no_skip_condition:
        return False

    for when in skip_conditions:
        condition = evaluate_when_rules(when['when'], schema, metadata, answer_store,
                                        group_instance, group_instance_id, routing_path)
        if condition is True:
            return True
    return False


def _get_when_rule_value(when_rule, group_instance, answer_store, schema, metadata, group_instance_id=None, routing_path=None):
    """
    Get the value from a when rule.
    :raises: Exception if none of `id`, `meta`, or `answer_count` are provided.
    :return: The value to use in a when rule
    """
    if 'id' in when_rule:
        value = get_answer_store_value(when_rule['id'], answer_store, schema, group_instance, group_instance_id, routing_path=routing_path)
    elif 'meta' in when_rule:
        value = get_metadata_value(metadata, when_rule['meta'])
    elif 'answer_count' in when_rule:
        value = answer_store.filter(answer_ids=[when_rule['answer_count']]).count()
    else:
        raise Exception('The when rule is invalid')

    return value


def evaluate_when_rules(when_rules, schema, metadata, answer_store, group_instance, group_instance_id=None, routing_path=None):
    """
    Whether the skip condition has been met.
    :param when_rules: when rules to evaluate
    :param schema: survey schema
    :param metadata: metadata for evaluating rules with metadata conditions
    :param answer_store: store of answers to evaluate
    :param group_instance: when evaluating a when rule for a repeating group
           this holds the group instance of the repeating group
    :param group_instance_id: The group instance ID to filter results by
    :param routing_path: The routing path to use when filtering answer_store
    :return: True if the when condition has been met otherwise False
    """
    for when_rule in when_rules:
        if 'id' in when_rule:
            if group_instance > 0 and not schema.answer_is_in_repeating_group(when_rule['id']):
                group_instance = 0

        value = _get_when_rule_value(when_rule, group_instance, answer_store, schema, metadata, group_instance_id, routing_path=routing_path)

        if 'date_comparison' in when_rule:
            if not evaluate_date_rule(when_rule, answer_store, schema, group_instance, metadata, value):
                return False
        elif 'comparison_id' in when_rule:
            comparison_id_value = _get_comparison_id_value(when_rule, answer_store, schema, group_instance, group_instance_id)
            if not evaluate_comparison_rule(when_rule, value, comparison_id_value):
                return False
        else:
            if not evaluate_rule(when_rule, value):
                return False

    return True


def get_answer_store_value(answer_id, answer_store, schema, group_instance, group_instance_id=None, routing_path=None):

    filtered = answer_store.filter(answer_ids=[answer_id])

    if routing_path:
        answers_on_path = _get_answers_on_path(filtered, schema, routing_path)
    else:
        answers_on_path = filtered

    if not answers_on_path.count():
        return None

    if all([answer.get('group_instance_id') for answer in answers_on_path.answers]) and group_instance_id:
        # If all of the matching answers have a group_instance_id, then we know the answer has this group_instance_id
        group_instance = None
        answer_block_id = schema.get_block_id_for_answer_id(answer_id)
        if not schema.answer_is_in_repeating_group(answer_id) and schema.block_drives_multiple_groups(answer_block_id):
            group_instance_id = None

    else:
        # We don't have group_instance_ids everywhere, so filter on the group_instance
        if group_instance > 0 and not schema.answer_is_in_repeating_group(answer_id):
            # If we're comparing to answer outside repeating group we may have an incorrect group_instance
            group_instance = 0

        group_instance_id = None

    filtered = answers_on_path.filter(answer_ids=[answer_id],
                                      group_instance=group_instance,
                                      group_instance_id=group_instance_id)

    if filtered.count() > 1:
        raise Exception('Multiple answers ({:d}) found evaluating when rule for answer ({})'
                        .format(filtered.count(), answer_id))

    return filtered[0]['value'] if filtered.count() == 1 else None


def get_number_of_repeats(group, schema, routing_path, answer_store):
    repeating_rule = schema.get_repeat_rule(group)

    if repeating_rule:
        return evaluate_repeat(repeating_rule, answer_store, schema, routing_path)

    return 1


def get_answer_ids_on_routing_path(schema, path):
    answer_ids_on_path = []
    for location in path:
        answer_ids_on_path.extend(
            schema.get_answers_by_id_for_block(location.block_id))

    return answer_ids_on_path


def get_metadata_value(metadata, key):
    return metadata.get(key)


def is_goto_rule(rule):
    return any(key in rule.get('goto', {}) for key in ('when', 'block', 'group'))
