import uuid


def convert_tx_id(tx_id):
    """
    Converts the guid tx_id to string of 16 characters with a dash between every 4 characters
    :param tx_id: tx_id to be converted
    :return: String in the form of xxxx-xxxx-xxxx-xxxx
    """
    return (tx_id[:4] + '-' + tx_id[4:])[:19]


def convert_tx_id_for_boxes(tx_id):
    """
    Converts the guid tx_id to string of 16 characters with a space between every 4 characters
    :param tx_id: tx_id to be converted
    :return: String in the form of xxxx xxxx xxxx xxxx
    """
    tx_id = uuid.UUID(tx_id)
    tx_id = tx_id.hex
    tx_id = tx_id.upper()
    displayable_tx_id = (tx_id[i:i + 4] for i in range(0, 16, 4))
    return displayable_tx_id


# Converts a dict into an object with the key names as property names
class ObjectFromDict:
    def __init__(self, properties):
        self.__dict__ = properties
