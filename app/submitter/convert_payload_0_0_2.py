

def convert_answers_to_payload_0_0_2(answer_store, schema, routing_path):
    """
    Convert answers into the data format below
    'data': [
        {
            'value': 'Joe Bloggs',
            'answer_id': 'household-full-name',
            'group_instance': 0,
            'answer_instance': 0
        },
        {
            'value': 'Fred Flintstone',
            'answer_id': 'household-full-name',
            'group_instance': 0,
            'answer_instance': 1
        },
        {
            'value': 'Husband or wife',
            'answer_id': 'who-is-related',
            'group_instance': 0,
            'answer_instance': 0
        }
    ]
    :param answer_store: questionnaire answers
    :param routing_path: the path followed in the questionnaire
    :return: data in a formatted form
    """
    data = []
    for location in routing_path:
        answer_ids = schema.get_answer_ids_for_block(location.block_id)
        answers_in_block = answer_store.filter(answer_ids, location.group_instance)
        data.extend(answers_in_block)
    return data
