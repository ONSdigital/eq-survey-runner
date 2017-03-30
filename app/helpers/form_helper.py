from werkzeug.datastructures import MultiDict

from app.helpers.schema_helper import SchemaHelper
from app.forms.household_composition_form import generate_household_composition_form, deserialise_composition_answers
from app.forms.household_relationship_form import build_relationship_choices, deserialise_relationship_answers, generate_relationship_form
from app.forms.questionnaire_form import generate_form


def get_form_for_location(block_json, location, answer_store, error_messages, disable_mandatory=False):
    """
    Returns the form necessary for the location given a get request, plus any template arguments

    :param disable_mandatory: Make mandatory answers optional
    :param error_messages: The default error messages to use within the form
    :param block_json: The block json
    :param location: The location which this form is for
    :param answer_store: The current answer store
    :return: form, template_args A tuple containing the form for this location and any additional template arguments
    """
    if disable_mandatory:
        block_json = disable_mandatory_answers(block_json)

    if location.block_id == 'household-composition':
        answers = answer_store.filter(location=location)

        data = deserialise_composition_answers(answers)

        return generate_household_composition_form(block_json, data, error_messages), None
    elif location.block_id in ['relationships', 'household-relationships']:

        answers = answer_store.filter(location=location)

        data = deserialise_relationship_answers(answers)

        choices = build_relationship_choices(answer_store, location.group_instance)

        form = generate_relationship_form(block_json, len(choices), data, error_messages)

        return form, {'relation_instances': choices}
    else:
        mapped_answers = answer_store.map(
            group_id=location.group_id,
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

        mapped_answers = deserialise_dates(block_json, mapped_answers)

        return generate_form(block_json, mapped_answers, error_messages), None


def post_form_for_location(block_json, location, answer_store, request_form, error_messages, disable_mandatory=False):
    """
    Returns the form necessary for the location given a post request, plus any template arguments

    :param disable_mandatory: Make mandatory answers optional
    :param error_messages: The default error messages to use within the form
    :param block_json: The block json
    :param location: The location which this form is for
    :param answer_store: The current answer store
    :param request_form: form, template_args A tuple containing the form for this location and any additional template arguments
    """
    if disable_mandatory:
        block_json = disable_mandatory_answers(block_json)

    if location.block_id == 'household-composition':
        return generate_household_composition_form(block_json, request_form, error_messages), None
    elif location.block_id in ['relationships', 'household-relationships']:
        choices = build_relationship_choices(answer_store, location.group_instance)
        form = generate_relationship_form(block_json, len(choices), request_form, error_messages)

        return form, {'relation_instances': choices}
    else:
        data = clear_other_text_field(request_form, SchemaHelper.get_questions_for_block(block_json))
        return generate_form(block_json, data, error_messages), None


def disable_mandatory_answers(block_json):
    for section_json in block_json.get('sections', []):
        for question_json in section_json['questions']:
            for answer_json in question_json['answers']:
                if 'mandatory' in answer_json and answer_json['mandatory'] is True:
                    answer_json['mandatory'] = False
    return block_json


def deserialise_dates(block_json, mapped_answers):
    answer_json_list = SchemaHelper.get_answers_for_block(block_json)

    # Deserialise all dates from the store
    date_answer_ids = [a['id'] for a in answer_json_list if a['type'] == "Date" or a['type'] == 'MonthYearDate']

    for date_answer_id in date_answer_ids:
        if date_answer_id in mapped_answers:
            substrings = mapped_answers[date_answer_id].split("/")

            if len(substrings) == 3:
                del mapped_answers[date_answer_id]
                mapped_answers.update({
                    '{answer_id}-day'.format(answer_id=date_answer_id): substrings[0],
                    '{answer_id}-month'.format(answer_id=date_answer_id): substrings[1].lstrip("0"),
                    '{answer_id}-year'.format(answer_id=date_answer_id): substrings[2],
                })
            elif len(substrings) == 2:
                del mapped_answers[date_answer_id]
                mapped_answers.update({
                    '{answer_id}-month'.format(answer_id=date_answer_id): substrings[0].lstrip("0"),
                    '{answer_id}-year'.format(answer_id=date_answer_id): substrings[1],
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
