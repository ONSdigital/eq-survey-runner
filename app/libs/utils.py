from flask import request
from config import LANGUAGES


def get_locale():
    return request.accept_languages.best_match(LANGUAGES.keys()) or 'cy'


# Converts a dict into an object with the key names as property names
class ObjectFromDict(object):
    def __init__(self, properties):
        self.__dict__ = properties


def eq_helper_lists_equivalent(list_a, list_b):
    """
    Compares two lists and returns a boolean indication of whether they are equivalent
    """
    if list_a is None and list_b is None:
        return True

    if list_a is not None and list_b is not None:
        if len(list_a) != len(list_b):
            return False

        for index, value in enumerate(list_a):
            if value != list_b[index]:
                return False

        return True
    else:
        return False


def eq_helper_dicts_equivalent(dict_a, dict_b):
    """
    Compares two dicts and returns a boolean indication of whether they are equivalent
    """
    if dict_a is None and dict_b is None:
        return True

    if dict_a is not None and dict_b is not None:
        if len(dict_a) != len(dict_b):
            return False

        for key, value in dict_a.items():
            if key not in dict_b.keys() or dict_b[key] != value:
                return False

        return True
    else:
        return False
