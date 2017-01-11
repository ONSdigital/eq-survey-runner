import uuid

from flask import request

from config import LANGUAGES


def get_locale():
    return request.accept_languages.best_match(LANGUAGES.keys()) or 'cy'


def convert_tx_id(tx_id):
    # converts the guid tx_id to string of 16 characters with a space between every 4 characters
    tx_id = uuid.UUID(tx_id)
    tx_id = tx_id.hex
    tx_id = tx_id.upper()
    displayable_tx_id = (tx_id[i:i+4] for i in range(0, 16, 4))
    return displayable_tx_id


# Converts a dict into an object with the key names as property names
class ObjectFromDict(object):
    def __init__(self, properties):
        self.__dict__ = properties
