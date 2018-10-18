from collections import OrderedDict
from datetime import datetime


def convert_answers_to_payload_0_0_1(answer_store, schema, routing_path):
    """
    Convert answers into the data format below
    'data': {
          '001': '01-01-2016',
          '002': '30-03-2016'
        }
    :param answer_store: questionnaire answers
    :param schema: QuestionnaireSchema class with popuated schema json
    :param routing_path: the path followed in the questionnaire
    :return: data in a formatted form
    """
    data = OrderedDict()
    for location in routing_path:
        answer_ids = schema.get_answer_ids_for_block(location.block_id)
        answers_in_block = answer_store.filter(answer_ids, location.group_instance)
        answer_schema_list = schema.get_answers_by_id_for_block(location.block_id)

        for answer in answers_in_block:
            answer_schema = answer_schema_list[answer['answer_id']]

            value = answer['value']

            if answer_schema is not None and value is not None and 'parent_answer_id' not in answer_schema:
                if answer_schema['type'] == 'Checkbox':
                    data.update(_get_checkbox_answer_data(answer_store, answer_schema, value))
                elif 'q_code' in answer_schema:
                    answer_data = _get_answer_data(data, answer_schema['q_code'], value)
                    if answer_data is not None:
                        data[answer_schema['q_code']] = _format_downstream_answer(answer_schema['type'], answer['value'], answer_data)

    return data


def _format_downstream_answer(answer_type, answer_value, answer_data):
    if answer_type == 'Date':
        return datetime.strptime(answer_value, '%Y-%m-%d').strftime('%d/%m/%Y')

    if answer_type == 'MonthYearDate':
        return datetime.strptime(answer_value, '%Y-%m').strftime('%m/%Y')

    return answer_data


def _get_answer_data(original_data, item_code, value):
    if item_code in original_data:
        data_to_return = original_data[item_code]
        if not isinstance(data_to_return, list):
            data_to_return = [data_to_return]
        data_to_return.append(_encode_value(value))

        return data_to_return
    return _encode_value(value)


def _get_checkbox_answer_data(answer_store, answer_schema, value):
    qcodes_and_values = []
    for user_answer in value:
        # find the option in the schema which matches the users answer
        option = next((option for option in answer_schema['options'] if option['value'] == user_answer), None)

        if option:
            if 'child_answer_id' in option:
                filtered = answer_store.filter(answer_ids=[option['child_answer_id']])

                if filtered.count() > 1:
                    raise Exception('Multiple answers found for {}'.format(option['child_answer_id']))

                # if the user has selected 'other' we need to find the child value it refers to.
                # the child value can be empty, in this case we just use the main value (e.g. other)
                user_answer = filtered[0]['value'] or user_answer

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
