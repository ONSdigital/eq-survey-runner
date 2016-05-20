from flask import request
from config import LANGUAGES


def get_locale():
    return request.accept_languages.best_match(LANGUAGES.keys()) or 'cy'


# Converts a dict into an object with the key names as property names
class ObjectFromDict(object):
    def __init__(self, properties):
        self.__dict__ = properties
