import random
from string import ascii_letters

from structlog import get_logger

from app.settings import EQ_LIST_ITEM_ID_LENGTH

logger = get_logger()


def random_string(length):
    return ''.join(random.choice(ascii_letters) for _ in range(length))


class ListStore:
    """ Storage for lists.
    """

    def __init__(self, existing_items=None):
        if not existing_items:
            existing_items = []

        self._lists = dict(existing_items)

    def __getitem__(self, item):
        try:
            return self._lists[item]
        except KeyError:
            return list()

    def _generate_identifier(self):
        """ Generate an unused random 6 character string"""
        while True:
            candidate = random_string(EQ_LIST_ITEM_ID_LENGTH)
            if candidate not in self.list_item_ids():
                return candidate

    def list_item_ids(self):
        ids = []
        for named_list in self._lists.values():
            ids.extend(named_list)

        return ids

    def delete_list_item_id(self, list_name, item_id):
        self._lists[list_name].remove(item_id)
        if not self._lists[list_name]:
            del self._lists[list_name]

    def add_list_item(self, list_name):
        """ Add a new list item to a named list.
        If the list does not exist, it will be created

        Returns:
            list item identifier for the new item
        """
        named_list = self._lists.get(list_name, [])

        new_list_identifier = self._generate_identifier()

        named_list.append(new_list_identifier)

        self._lists[list_name] = named_list

        return new_list_identifier

    def serialise(self):
        return [{'name': name, 'items': list_items} for name, list_items in self._lists.items()]

    @classmethod
    def deserialise(cls, serialised: list):
        if not serialised:
            return cls()

        deserialised = []
        for named_list in serialised:
            deserialised.append((named_list['name'], named_list['items']))

        return cls(existing_items=deserialised)
