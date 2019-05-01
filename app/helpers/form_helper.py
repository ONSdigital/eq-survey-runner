from collections import OrderedDict

from structlog import get_logger
from werkzeug.datastructures import MultiDict

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

    mapped_answers = get_mapped_answers(
        schema,
        answer_store,
        location=location,
    )

    return generate_form(schema, block_json.get('question'), answer_store, metadata, data=mapped_answers)


def post_form_for_block(schema, block_json, answer_store, metadata, request_form, disable_mandatory=False):
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

    question = block_json.get('question')

    data = clear_detail_answer_field(request_form, question)

    return generate_form(schema, question, answer_store, metadata, formdata=data)


def disable_mandatory_answers(block):

    def set_mandatory_to_false(question):
        # Here Be Dragons: This loop modifies the input in place.
        for answer in question.get('answers', []):
            if answer.get('mandatory', True) is True:
                answer['mandatory'] = False

    if block.get('question'):
        set_mandatory_to_false(block['question'])

    return block


def clear_detail_answer_field(data, question):
    """
    Checks the submitted answers and in the case of both checkboxes and radios,
    removes the text entered into the detail answer field if the associated option is not
    selected.
    :param data: the submitted form data.
    :param question: a question to clear.
    :return: the form data with the other text field cleared, if appropriate.
    """
    form_data = MultiDict(data)
    if question:
        for answer in question.get('answers', []):
            for option in answer.get('options', []):
                if 'detail_answer' in option:
                    if option['value'] not in form_data.getlist(answer['id']):
                        form_data[option['detail_answer']['id']] = ''

    return form_data


def get_mapped_answers(schema, answer_store, location):
    """
    Maps the answers in an answer store to a dictionary of key, value answers.
    """

    block_id = location.block_id

    answer_ids = schema.get_answer_ids_for_block(block_id)

    answers = answer_store.get_answers_by_answer_id(answer_ids=answer_ids, list_item_id=location.list_item_id)
    result = {answer.answer_id: answer.value for answer in answers if answer}

    return OrderedDict(sorted(result.items()))
