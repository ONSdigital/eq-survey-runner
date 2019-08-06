def convert_tx_id(tx_id):
    """
    Converts the guid tx_id to string of 16 characters with a dash between every 4 characters
    :param tx_id: tx_id to be converted
    :return: String in the form of xxxx-xxxx-xxxx-xxxx
    """
    return (tx_id[:4] + '-' + tx_id[4:])[:19]


# Converts a dict into an object with the key names as property names
class ObjectFromDict:
    def __init__(self, properties):
        self.__dict__ = properties


def get_answer(schema, answer_store, answer_id, list_item_id=None):
    if (
        list_item_id
        and not schema.is_answer_in_list_collector_block(answer_id)
        and not schema.is_answer_in_repeating_section(answer_id)
    ):
        list_item_id = None

    answer = answer_store.get_answer(answer_id, list_item_id)

    return answer
