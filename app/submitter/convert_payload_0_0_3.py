from typing import List, Dict

from app.data_model.answer_store import AnswerStore


def convert_answers_to_payload_0_0_3(
    answer_store, list_store, schema, full_routing_path
) -> List[Dict]:
    """
    Convert answers into the data format below
    'data': [
        {
            'value': 'Joe',
            'answer_id': 'first-name',
            'list_item_id': 'axkkdh'
        },
        {
            'value': 'Dimaggio',
            'answer_id': 'last-name',
            'list_item_id': 'axkkdh'
        },
        {
            'value': 'No',
            'answer_id': 'do-you-live-here'
        }
    ]

    For list answers, this method will query the list store and get all answers from the
    add list item block. If there are multiple list collectors for one list, they will have
    the same answer_ids, and will not be duplicated.

    Returns:
        A list of answer dictionaries.
    """
    answers_payload = AnswerStore()

    for location in full_routing_path:

        add_list_collector_answers(
            answer_store, list_store, schema, location, answers_payload
        )

        answer_ids = schema.get_answer_ids_for_block(location.block_id)
        answers_in_block = answer_store.get_answers_by_answer_id(
            answer_ids, list_item_id=location.list_item_id
        )
        for answer_in_block in answers_in_block:
            answers_payload.add_or_update(answer_in_block)

    return list(answers_payload.answer_map.values())


def add_list_collector_answers(
    answer_store, list_store, schema, location, answers_payload
):
    """ Add answers from list_collector for a specific location.
    Output is added to the `answers_payload` argument."""
    list_collector_block = schema.get_block(location.block_id)
    block_type = list_collector_block['type']

    if schema.is_list_block_type(block_type) or schema.is_primary_person_block_type(
        block_type
    ):
        answers_ids_in_add_block = schema.get_answer_ids_for_list_items(
            list_collector_block['id']
        )
        list_name = list_collector_block['for_list']
        list_item_ids = list_store[list_name].items

        for list_item_id in list_item_ids:
            for answer_id in answers_ids_in_add_block:
                answer = answer_store.get_answer(answer_id, list_item_id)
                if answer:
                    answers_payload.add_or_update(answer)
