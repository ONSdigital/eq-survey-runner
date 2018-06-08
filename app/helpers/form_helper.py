from collections import OrderedDict
from structlog import get_logger
from werkzeug.datastructures import MultiDict


from app.data_model.answer_store import natural_order
from app.forms.household_composition_form import generate_household_composition_form, deserialise_composition_answers
from app.forms.household_relationship_form import build_relationship_choices, deserialise_relationship_answers, generate_relationship_form
from app.forms.questionnaire_form import generate_form

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

        return generate_household_composition_form(schema, block_json, data)

    elif location.block_id in ['relationships', 'household-relationships']:
        answer_ids = schema.get_answer_ids_for_block(location.block_id)
        answers = answer_store.filter(answer_ids, location.group_instance)

        data = deserialise_relationship_answers(answers)

        relationship_choices = build_relationship_choices(answer_store, location.group_instance)

        form = generate_relationship_form(schema, block_json, relationship_choices, data)

        return form

    mapped_answers = get_mapped_answers(
        schema,
        answer_store,
        group_instance=location.group_instance,
        block_id=location.block_id,
    )

    # Form generation expects post like data, so cast answers to strings
    for answer_id, mapped_answer in mapped_answers.items():
        if isinstance(mapped_answer, list):
            for index, element in enumerate(mapped_answer):
                mapped_answers[answer_id][index] = str(element)
        else:
            mapped_answers[answer_id] = str(mapped_answer)

    mapped_answers = deserialise_dates(schema, location.block_id, mapped_answers)

    return generate_form(schema, block_json, mapped_answers, answer_store, metadata)


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
        return generate_household_composition_form(schema, block_json, request_form)

    elif location.block_id in ['relationships', 'household-relationships']:
        relationship_choices = build_relationship_choices(answer_store, location.group_instance)
        form = generate_relationship_form(schema, block_json, relationship_choices, request_form)

        return form

    data = clear_other_text_field(request_form, schema.get_questions_for_block(block_json))
    return generate_form(schema, block_json, data, answer_store, metadata)


def disable_mandatory_answers(block_json):
    for question_json in block_json.get('questions', []):
        for answer_json in question_json['answers']:
            if 'mandatory' in answer_json and answer_json['mandatory'] is True:
                answer_json['mandatory'] = False
    return block_json


def deserialise_dates(schema, block_id, mapped_answers):
    answer_json_list = schema.get_answers_for_block(block_id)

    # Deserialise all dates from the store
    date_answer_ids = [a['id'] for a in answer_json_list if a['type'] in ['Date', 'MonthYearDate', 'YearDate']]

    for date_answer_id in date_answer_ids:
        if date_answer_id in mapped_answers:
            substrings = mapped_answers[date_answer_id].split('-')

            del mapped_answers[date_answer_id]
            if len(substrings) == 3:
                mapped_answers.update({
                    '{answer_id}-year'.format(answer_id=date_answer_id): substrings[0],
                    '{answer_id}-month'.format(answer_id=date_answer_id): substrings[1].lstrip('0'),
                    '{answer_id}-day'.format(answer_id=date_answer_id): substrings[2],
                })
            if len(substrings) == 2:
                mapped_answers.update({
                    '{answer_id}-year'.format(answer_id=date_answer_id): substrings[0],
                    '{answer_id}-month'.format(answer_id=date_answer_id): substrings[1].lstrip('0'),
                })
            if len(substrings) == 1:
                mapped_answers.update({
                    '{answer_id}-year'.format(answer_id=date_answer_id): substrings[0],
                })

    return mapped_answers


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
        for answer in question['answers']:
            if 'parent_answer_id' in answer and \
                    answer['parent_answer_id'] in data and \
                    'Other' not in form_data.getlist(answer['parent_answer_id']) and \
                    form_data.get(answer['id']):

                form_data[answer['id']] = ''

    return form_data


def get_mapped_answers(schema, answer_store, block_id, group_instance):
    """
    Maps the answers in an answer store to a dictionary of key, value answers. Keys include instance
    id's when the instance id is non zero.

    :param answer_id:
    :param block_id:
    :param group_id:
    :param answer_instance:
    :param group_instance:
    :return:
    """
    answer_ids = schema.get_answer_ids_for_block(block_id)

    result = {}
    for answer in answer_store.filter(answer_ids=answer_ids,
                                      group_instance=group_instance):
        answer_id = answer['answer_id']
        answer_id += '_' + str(answer['answer_instance']) if answer['answer_instance'] > 0 else ''

        result[answer_id] = answer['value']

    return OrderedDict(sorted(result.items(), key=lambda t: natural_order(t[0])))
