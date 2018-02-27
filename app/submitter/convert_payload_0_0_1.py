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
                if 'q_code' in answer_schema and (answer_schema['type'] != 'Checkbox' or any('q_code' not in option for option in
                                                                                             answer_schema['options'])):

                    answer_data = _get_answer_data(data, answer_schema['q_code'], value)
                    if answer_data is not None:
                        data[answer_schema['q_code']] = _format_downstream_answer(answer_schema['type'], answer['value'], answer_data)
                else:
                    data.update(_get_checkbox_answer_data(answer_store, answer_schema, value))
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


def _get_checkbox_answer_data(answer_store, checkboxes_with_qcode, value):

    checkbox_answer_data = OrderedDict()

    for user_answer in value:
        # find the option in the schema which matches the users answer
        option = next((option for option in checkboxes_with_qcode['options'] if option['value'] == user_answer), None)

        if option:
            if 'child_answer_id' in option:
                filtered = answer_store.filter(answer_ids=[option['child_answer_id']])

                if filtered.count() > 1:
                    raise Exception('Multiple answers found for {}'.format(option['child_answer_id']))

                # if the user has selected 'other' we need to find the value it refers to.
                # when non-mandatory, the other box value can be empty, in this case we just use its value
                checkbox_answer_data[option['q_code']] = option['value']
            else:
                checkbox_answer_data[option['q_code']] = user_answer

    return checkbox_answer_data


def _encode_value(value):
    if isinstance(value, str):
        if value == '':
            return None
        return value
    return str(value)
