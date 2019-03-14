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
    :param answer_value: the left hand operand in the comparison
    :param match_value: the right hand operand in the comparison
    :return: boolean value of comparing lhs and rhs using the specified operator
    """
    answer_and_match = answer_value is not None and match_value is not None

    comparison_operators = {
        'equals': lambda answer_value, match_value: answer_value == match_value,
        'not equals': lambda answer_value, match_value: answer_value != match_value,
        'contains': lambda answer_value, match_value: isinstance(answer_value, list) and match_value in answer_value,
        'not contains': lambda answer_value, match_value: isinstance(answer_value, list) and match_value not in answer_value,
        'set': lambda answer_value, _: answer_value is not None and answer_value != [],
        'not set': lambda answer_value, _: answer_value is None or answer_value == [],
        'greater than': lambda answer_value, match_value: answer_and_match and answer_value > match_value,
        'greater than or equal to': lambda answer_value, match_value: answer_and_match and answer_value >= match_value,
        'less than': lambda answer_value, match_value: answer_and_match and answer_value < match_value,
        'less than or equal to': lambda answer_value, match_value: answer_and_match and answer_value <= match_value,
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
        match_value = get_answer_store_value(date_comparison['id'], answer_store, schema)
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


def evaluate_goto(goto_rule, schema, metadata, answer_store, routing_path=None):
    """
    Determine whether a goto rule will be satisfied based on a given answer
    :param goto_rule: goto rule to evaluate
    :param schema: survey schema
    :param metadata: metadata for evaluating rules with metadata conditions
    :param answer_store: store of answers to evaluate
    :return: True if the when condition has been met otherwise False
    """
    if 'when' in goto_rule:
        return evaluate_when_rules(
            goto_rule['when'],
            schema,
            metadata,
            answer_store,
            routing_path=routing_path,
        )
    return True


def _get_answers_on_path(answers, schema, routing_path) -> AnswerStore:
    """
    Get any answers that are on the routing path and return an answer store.
    """
    answers_to_remove = [answer for answer in answers if not _is_answer_on_path(schema, answer, routing_path)]

    answers_on_path = answers.copy()

    for answer in answers_to_remove:
        answers_on_path.remove_answer(answer)

    return answers_on_path


def _is_answer_on_path(schema, answer, routing_path):
    answer_schema = schema.get_answer(answer['answer_id'])
    question_schema = schema.get_question(answer_schema['parent_id'])
    block_schema = schema.get_block(question_schema['parent_id'])
    location = Location(block_id=block_schema['id'])
    return location in routing_path


def _get_comparison_id_value(when_rule, answer_store, schema):
    """
        Gets the value of an answer specified as an operand in a comparator ( i.e right hand argument ,
        or rhs in if lhs>rhs ) In a when clause
    """
    answer_id = when_rule['comparison_id']

    return get_answer_store_value(answer_id, answer_store, schema)


def evaluate_skip_conditions(skip_conditions, schema, metadata, answer_store, routing_path=None):
    """
    Determine whether a skip condition will be satisfied based on a given answer
    :param skip_conditions: skip_conditions rule to evaluate
    :param schema: survey schema
    :param metadata: metadata for evaluating rules with metadata conditions
    :param answer_store: store of answers to evaluate
    :return: True if the when condition has been met otherwise False
    """

    no_skip_condition = skip_conditions is None or len(skip_conditions) == 0
    if no_skip_condition:
        return False

    for when in skip_conditions:
        condition = evaluate_when_rules(when['when'], schema, metadata, answer_store, routing_path)
        if condition is True:
            return True
    return False


def _get_when_rule_value(when_rule, answer_store, schema, metadata, routing_path=None):
    """
    Get the value from a when rule.
    :raises: Exception if none of `id` or `meta` are provided.
    :return: The value to use in a when rule
    """
    if 'id' in when_rule:
        value = get_answer_store_value(when_rule['id'], answer_store, schema, routing_path=routing_path)
    elif 'meta' in when_rule:
        value = get_metadata_value(metadata, when_rule['meta'])
    else:
        raise Exception('The when rule is invalid')

    return value


def evaluate_when_rules(when_rules, schema, metadata, answer_store, routing_path=None):
    """
    Whether the skip condition has been met.
    :param when_rules: when rules to evaluate
    :param schema: survey schema
    :param metadata: metadata for evaluating rules with metadata conditions
    :param answer_store: store of answers to evaluate
    :param routing_path: The routing path to use when filtering answer_store
    :return: True if the when condition has been met otherwise False
    """
    for when_rule in when_rules:
        value = _get_when_rule_value(when_rule, answer_store, schema, metadata, routing_path=routing_path)

        if 'date_comparison' in when_rule:
            if not evaluate_date_rule(when_rule, answer_store, schema, metadata, value):
                return False
        elif 'comparison_id' in when_rule:
            comparison_id_value = _get_comparison_id_value(when_rule, answer_store, schema)
            if not evaluate_comparison_rule(when_rule, value, comparison_id_value):
                return False
        else:
            if not evaluate_rule(when_rule, value):
                return False

    return True


def get_answer_store_value(answer_id, answer_store, schema, routing_path=None):

    filtered = answer_store.filter(answer_ids=[answer_id])

    if routing_path:
        answers_on_path = _get_answers_on_path(filtered, schema, routing_path)
    else:
        answers_on_path = filtered

    if not answers_on_path.count():
        return None

    filtered = answers_on_path.filter(answer_ids=[answer_id])

    return next(iter(filtered))['value'] if filtered.count() == 1 else None


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
