import logging
import re
from datetime import datetime

from dateutil.relativedelta import relativedelta

from app.questionnaire.location import Location

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

    match_value = when.get('value', when.get('values'))

    condition = when['condition']
    # Evaluate the condition on the routing rule
    return evaluate_condition(condition, answer_value, match_value)


def evaluate_date_rule(when, answer_store, schema, metadata, answer_value):
    date_comparison = when['date_comparison']

    answer_value = convert_to_datetime(answer_value)
    match_value = get_date_match_value(date_comparison, answer_store, schema, metadata)
    condition = when.get('condition')

    if not answer_value or not match_value or not condition:
        return False

    # Evaluate the condition on the routing rule
    return evaluate_condition(condition, answer_value, match_value)


def evaluate_condition(condition, answer_value, match_value):
    """
    :param condition: string representation of comparison operator
    :param answer_value: the left hand side operand in the comparison
    :param match_value: the right hand side operand in the comparison
    :return: boolean value of comparing lhs and rhs using the specified operator
    """
    answer_and_match = answer_value is not None and match_value is not None

    comparison_operators = {
        'equals': lambda answer_value, match_value: answer_value == match_value,
        'not equals': lambda answer_value, match_value: answer_value != match_value,
        'equals any': lambda answer_value, match_values: answer_value in match_values,
        'not equals any': lambda answer_value, match_values: answer_value
        not in match_values,
        'contains': lambda answer_values, match_value: answer_and_match
        and match_value in answer_values,
        'not contains': lambda answer_values, match_value: answer_and_match
        and match_value not in answer_values,
        'contains any': lambda answer_values, match_values: answer_and_match
        and any(match_value in answer_values for match_value in match_values),
        'contains all': lambda answer_values, match_values: answer_and_match
        and all(match_value in answer_values for match_value in match_values),
        'set': lambda answer_value, _: answer_value not in (None, []),
        'not set': lambda answer_value, _: answer_value in (None, []),
        'greater than': lambda answer_value, match_value: answer_and_match
        and answer_value > match_value,
        'greater than or equal to': lambda answer_value, match_value: answer_and_match
        and answer_value >= match_value,
        'less than': lambda answer_value, match_value: answer_and_match
        and answer_value < match_value,
        'less than or equal to': lambda answer_value, match_value: answer_and_match
        and answer_value <= match_value,
    }

    match_function = comparison_operators[condition]

    return match_function(answer_value, match_value)


def get_date_match_value(date_comparison, answer_store, schema, metadata):
    match_value = None

    if 'value' in date_comparison:
        if date_comparison['value'] == 'now':
            match_value = datetime.utcnow().strftime('%Y-%m-%d')
        else:
            match_value = date_comparison['value']
    elif 'id' in date_comparison:
        match_value = get_answer_value(date_comparison['id'], answer_store, schema)
    elif 'meta' in date_comparison:
        match_value = get_metadata_value(metadata, date_comparison['meta'])

    match_value = convert_to_datetime(match_value)

    if 'offset_by' in date_comparison and match_value:
        offset = date_comparison['offset_by']
        match_value = match_value + relativedelta(
            days=offset.get('days', 0),
            months=offset.get('months', 0),
            years=offset.get('years', 0),
        )

    return match_value


def convert_to_datetime(value):
    date_format = '%Y-%m'
    if value and re.match(r'\d{4}-\d{2}-\d{2}', value):
        date_format = '%Y-%m-%d'
    if value and re.match(r'\d{4}$', value):
        date_format = '%Y'

    return datetime.strptime(value, date_format) if value else None


def evaluate_goto(
    goto_rule,
    schema,
    metadata,
    answer_store,
    list_store,
    current_location,
    routing_path=None,
):
    """
    Determine whether a goto rule will be satisfied based on a given answer
    :param goto_rule: goto rule to evaluate
    :param schema: survey schema
    :param metadata: metadata for evaluating rules with metadata conditions
    :param answer_store: store of answers to evaluate
    :param list_store: store of lists to evaluate
    :param current_location: the location to use when evaluating when rules
    :param routing_path: the routing path used to evaluate if answer is on the path
    :return: True if the when condition has been met otherwise False
    """
    if 'when' in goto_rule:
        return evaluate_when_rules(
            goto_rule['when'],
            schema,
            metadata,
            answer_store,
            list_store,
            current_location,
            routing_path=routing_path,
        )
    return True


def _is_answer_on_path(schema, answer, routing_path):
    block_id = schema.get_block_for_answer_id(answer.answer_id)['id']
    section_id = schema.get_section_id_for_block_id(block_id)
    list_name = schema.get_repeating_list_for_section(section_id)

    location = Location(
        section_id=section_id,
        block_id=block_id,
        list_item_id=answer.list_item_id,
        list_name=list_name,
    )
    return location in routing_path


def _get_comparison_id_value(
    when_rule, answer_store, schema, current_location=None, routing_path=None
):
    """
        Gets the value of a comparison id specified as an operand in a comparator
    """
    if current_location and when_rule['comparison']['source'] == 'location':
        try:
            return getattr(current_location, when_rule['comparison']['id'])
        except AttributeError:
            return None

    answer_id = when_rule['comparison']['id']
    list_item_id = current_location.list_item_id if current_location else None

    return get_answer_value(
        answer_id,
        answer_store,
        schema,
        routing_path=routing_path,
        list_item_id=list_item_id,
    )


def evaluate_skip_conditions(
    skip_conditions,
    schema,
    metadata,
    answer_store,
    list_store,
    current_location,
    routing_path=None,
):
    """
    Determine whether a skip condition will be satisfied based on a given answer
    :param skip_conditions: skip_conditions rule to evaluate
    :param schema: survey schema
    :param metadata: metadata for evaluating rules with metadata conditions
    :param answer_store: store of answers to evaluate
    :param list_store: store of lists to evaluate
    :param current_location: the location to use when evaluating when rules
    :param routing_path: the routing path used to evaluate if answer is on the path
    :return: True if the when condition has been met otherwise False
    """
    no_skip_condition = skip_conditions is None or len(skip_conditions) == 0

    if no_skip_condition:
        return False

    for when in skip_conditions:
        condition = evaluate_when_rules(
            when['when'],
            schema,
            metadata,
            answer_store,
            list_store,
            current_location,
            routing_path=routing_path,
        )
        if condition is True:
            return True
    return False


def _get_when_rule_value(
    when_rule,
    answer_store,
    list_store,
    schema,
    metadata,
    routing_path=None,
    list_item_id=None,
):
    """
    Get the value from a when rule.
    :raises: Exception if none of `id` or `meta` are provided.
    :return: The value to use in a when rule
    """
    if 'id' in when_rule:
        value = get_answer_value(
            when_rule['id'],
            answer_store,
            schema,
            routing_path=routing_path,
            list_item_id=list_item_id,
        )
    elif 'meta' in when_rule:
        value = get_metadata_value(metadata, when_rule['meta'])
    elif 'id_selector' in when_rule:
        value = getattr(list_store.get(when_rule['list']), when_rule['id_selector'])
    elif 'list' in when_rule:
        value = get_list_count(list_store, when_rule['list'])
    else:
        raise Exception('The when rule is invalid')

    return value


def evaluate_when_rules(
    when_rules,
    schema,
    metadata,
    answer_store,
    list_store,
    current_location=None,
    routing_path=None,
):
    """
    Whether the skip condition has been met.
    :param when_rules: when rules to evaluate
    :param schema: survey schema
    :param metadata: metadata for evaluating rules with metadata conditions
    :param answer_store: store of answers to evaluate
    :param list_store: store of lists to evaluate
    :param current_location: The location to use when evaluating when rules
    :param routing_path: The location to use when evaluating when rules
    :return: True if the when condition has been met otherwise False
    """
    for when_rule in when_rules:

        list_item_id = current_location.list_item_id if current_location else None

        value = _get_when_rule_value(
            when_rule,
            answer_store,
            list_store,
            schema,
            metadata,
            routing_path=routing_path,
            list_item_id=list_item_id,
        )

        if 'date_comparison' in when_rule:
            if not evaluate_date_rule(when_rule, answer_store, schema, metadata, value):
                return False
        elif 'comparison' in when_rule:
            comparison_id_value = _get_comparison_id_value(
                when_rule, answer_store, schema, current_location, routing_path
            )
            if not evaluate_comparison_rule(when_rule, value, comparison_id_value):
                return False
        else:
            if not evaluate_rule(when_rule, value):
                return False

    return True


def get_answer_for_answer_id(answer_id, answer_store, schema, list_item_id):
    list_item_id = schema.get_list_item_id_for_answer_id(answer_id, list_item_id)

    answer = answer_store.get_answer(
        answer_id, list_item_id
    ) or schema.get_default_answer(answer_id)

    return answer


def get_answer_value(
    answer_id, answer_store, schema, routing_path=None, list_item_id=None
):
    answer = get_answer_for_answer_id(answer_id, answer_store, schema, list_item_id)

    if not answer:
        return None

    if routing_path:
        if _is_answer_on_path(schema, answer, routing_path):
            return answer.value
    else:
        return answer.value


def get_metadata_value(metadata, key):
    return metadata.get(key)


def get_list_count(list_store, list_name):
    return len(list_store[list_name].items)


def is_goto_rule(rule):
    return any(key in rule.get('goto', {}) for key in ('when', 'block', 'group'))
