from collections import OrderedDict
from datetime import datetime

from app.questionnaire.schema_utils import choose_question_to_display


def convert_answers_to_payload_0_0_1(metadata, answer_store, schema, routing_path):
    """
    Convert answers into the data format below
    'data': {
          '001': '01-01-2016',
          '002': '30-03-2016'
        }
    :param metadata: questionnaire metadata
    :param answer_store: questionnaire answers
    :param schema: QuestionnaireSchema class with popuated schema json
    :param routing_path: the path followed in the questionnaire
    :return: data in a formatted form
    """
    data = OrderedDict()
    for location in routing_path:
        answer_ids = schema.get_answer_ids_for_block(location.block_id)
        answers_in_block = answer_store.filter(answer_ids)

        for answer_in_block in answers_in_block:
            answer_schema = None

            block = schema.get_block_for_answer_id(answer_in_block['answer_id'])
            question = choose_question_to_display(block, schema, metadata, answer_store)
            for answer in question['answers']:
                if answer['id'] == answer_in_block['answer_id']:
                    answer_schema = answer

            value = answer_in_block['value']

            if answer_schema is not None and value is not None:
                if answer_schema['type'] == 'Checkbox':
                    data.update(_get_checkbox_answer_data(answer_store, answer_schema, value))
                elif 'q_code' in answer_schema:
                    answer_data = _encode_value(value)
                    if answer_data is not None:
                        data[answer_schema['q_code']] = _format_downstream_answer(answer_schema['type'], answer_in_block['value'], answer_data)

    return data


def _format_downstream_answer(answer_type, answer_value, answer_data):
    if answer_type == 'Date':
        return datetime.strptime(answer_value, '%Y-%m-%d').strftime('%d/%m/%Y')

    if answer_type == 'MonthYearDate':
        return datetime.strptime(answer_value, '%Y-%m').strftime('%m/%Y')

    return answer_data


def _get_checkbox_answer_data(answer_store, answer_schema, value):
    qcodes_and_values = []
    for user_answer in value:
        # find the option in the schema which matches the users answer
        option = next((option for option in answer_schema['options'] if option['value'] == user_answer), None)

        if option:
            if 'detail_answer' in option:
                filtered = answer_store.filter(answer_ids=[option['detail_answer']['id']])

                # if the user has selected an option with a detail answer we need to find the detail answer value it refers to.
                # the detail answer value can be empty, in this case we just use the main value (e.g. other)
                user_answer = filtered.values()[0] or user_answer

            qcodes_and_values.append((option.get('q_code'), user_answer))

    checkbox_answer_data = OrderedDict()

    if all(q_code is not None for (q_code, _) in qcodes_and_values):
        checkbox_answer_data.update(qcodes_and_values)
    else:
        checkbox_answer_data[answer_schema['q_code']] = str([v for (_, v) in qcodes_and_values])

    return checkbox_answer_data


def _encode_value(value):
    if isinstance(value, str):
        if value == '':
            return None
        return value
    return str(value)
