from collections import OrderedDict

from structlog import get_logger
from werkzeug.datastructures import MultiDict


from app.data_model.answer_store import natural_order
from app.forms.household_composition_form import generate_household_composition_form, deserialise_composition_answers
from app.forms.household_relationship_form import build_relationship_choices, deserialise_relationship_answers, generate_relationship_form
from app.forms.questionnaire_form import generate_form
from app.helpers.schema_helpers import get_group_instance_id

logger = get_logger()


def get_form_for_location(schema, block_json, location, answer_store, metadata, disable_mandatory=False):  # pylint: disable=too-many-locals
    """
    Returns the form necessary for the location given a get request, plus any template arguments

    :param schema: schema
    :param block_json: The block json
    :param location: The location which this form is for
    :param answer_store: The current answer store
    :param metadata: metadata
    :param disable_mandatory: Make mandatory answers optional
    :return: form, template_args A tuple containing the form for this location and any additional template arguments
    """
    if disable_mandatory:
        block_json = disable_mandatory_answers(block_json)

    if location.block_id == 'household-composition':
        answer_ids = schema.get_answer_ids_for_block(location.block_id)
        answers = answer_store.filter(answer_ids, location.group_instance)

        data = deserialise_composition_answers(answers)

        return generate_household_composition_form(schema, block_json, data, metadata, location.group_instance)

    group_instance_id = get_group_instance_id(schema, answer_store, location)

    if schema.block_has_question_type(location.block_id, 'Relationship'):
        answer_ids = schema.get_answer_ids_for_block(location.block_id)
        group = schema.get_group(location.group_id)
        answers = answer_store.filter(answer_ids, location.group_instance)

        data = deserialise_relationship_answers(answers)

        # Relationship block only supports 1 question
        question = schema.get_question(block_json['questions'][0]['id'])

        answer_ids = []

        repeat_rule = group['routing_rules'][0]['repeat']
        if 'answer_ids' in repeat_rule:
            for answer_id in repeat_rule['answer_ids']:
                answer_ids.append(answer_id)
        if 'answer_id' in repeat_rule:
            answer_ids.append(repeat_rule['answer_id'])

        relationship_choices = build_relationship_choices(answer_ids, answer_store, location.group_instance, question.get('member_label'))

        form = generate_relationship_form(schema, block_json, relationship_choices, data, location.group_instance, group_instance_id)

        return form

    mapped_answers = get_mapped_answers(
        schema,
        answer_store,
        group_instance=location.group_instance,
        group_instance_id=group_instance_id,
        block_id=location.block_id,
    )

    return generate_form(schema, block_json, answer_store, metadata, location.group_instance, group_instance_id, data=mapped_answers)


def post_form_for_location(schema, block_json, location, answer_store, metadata, request_form, disable_mandatory=False):
    """
    Returns the form necessary for the location given a post request, plus any template arguments

    :param block_json: The block json
    :param location: The location which this form is for
    :param answer_store: The current answer store
    :param metadata: metadata
    :param request_form: form, template_args A tuple containing the form for this location and any additional template arguments
    :param error_messages: The default error messages to use within the form
    :param disable_mandatory: Make mandatory answers optional
    """

    if disable_mandatory:
        block_json = disable_mandatory_answers(block_json)

    if location.block_id == 'household-composition':
        return generate_household_composition_form(schema, block_json, request_form, metadata, location.group_instance)

    group_instance_id = get_group_instance_id(schema, answer_store, location)

    if schema.block_has_question_type(location.block_id, 'Relationship'):
        group = schema.get_group(location.group_id)

        answer_ids = []

        repeat_rule = group['routing_rules'][0]['repeat']
        if 'answer_ids' in repeat_rule:
            for answer_id in repeat_rule['answer_ids']:
                answer_ids.append(answer_id)
        if 'answer_id' in repeat_rule:
            answer_ids.append(repeat_rule['answer_id'])

        relationship_choices = build_relationship_choices(answer_ids, answer_store, location.group_instance)
        form = generate_relationship_form(schema, block_json, relationship_choices, request_form, location.group_instance, group_instance_id)

        return form

    data = clear_other_text_field(request_form, schema.get_questions_for_block(block_json))
    return generate_form(schema, block_json, answer_store, metadata, location.group_instance, group_instance_id, formdata=data)


def disable_mandatory_answers(block_json):
    for question_json in block_json.get('questions', []):
        for answer_json in question_json.get('answers', []):
            if 'mandatory' in answer_json and answer_json['mandatory'] is True:
                answer_json['mandatory'] = False
    return block_json


def clear_other_text_field(data, questions_for_block):
    """
    Checks the submitted answers and in the case of both checkboxes and radios,
    removes the text entered into the other text field if the Other option is not
    selected.
    :param data: the submitted form data.
    :param questions_for_block: a list of questions from the block schema.
    :return: the form data with the other text field cleared, if appropriate.
    """
    form_data = MultiDict(data)
    for question in questions_for_block:
        for answer in question.get('answers', []):
            if 'parent_answer_id' in answer and \
                    answer['parent_answer_id'] in data and \
                    'Other' not in form_data.getlist(answer['parent_answer_id']) and \
                    form_data.get(answer['id']):

                form_data[answer['id']] = ''

    return form_data


def get_mapped_answers(schema, answer_store, block_id, group_instance, group_instance_id):
    """
    Maps the answers in an answer store to a dictionary of key, value answers. Keys include instance
    id's when the instance id is non zero.

    :param answer_id:
    :param block_id:
    :param group_id:
    :param answer_instance:
    :param group_instance:
    :param group_instance_id:
    :return:
    """
    answer_ids = schema.get_answer_ids_for_block(block_id)

    result = {}
    for answer in answer_store.filter(answer_ids=answer_ids,
                                      group_instance=group_instance,
                                      group_instance_id=group_instance_id):
        answer_id = answer['answer_id']
        answer_id += '_' + str(answer['answer_instance']) if answer['answer_instance'] > 0 else ''

        result[answer_id] = answer['value']

    return OrderedDict(sorted(result.items(), key=lambda t: natural_order(t[0])))
