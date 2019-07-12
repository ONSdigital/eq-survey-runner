import random
from string import ascii_letters
from typing import List, Mapping, Optional

from structlog import get_logger

from app.settings import EQ_LIST_ITEM_ID_LENGTH

logger = get_logger()


def random_string(length):
    return ''.join(random.choice(ascii_letters) for _ in range(length))


class ListModel:
    def __init__(
        self,
        name: str,
        items: Optional[List] = None,
        primary_person: Optional[str] = None,
    ):
        self.name = name
        self.items = items or []
        self.primary_person = primary_person

    def __eq__(self, other):
        if not isinstance(other, ListModel):
            return NotImplemented
        return self.items == other.items and self.primary_person == other.primary_person

    def serialise(self):
        serialised = {'items': self.items, 'name': self.name}

        if self.primary_person:
            serialised['primary_person'] = self.primary_person

        return serialised

    def __repr__(self):
        return f'<ListModel name={self.name} items={self.items}, primary_person={self.primary_person}>'


class ListStore:
    """ Storage for lists.

    Stores in the form:

    ```
    self._lists: {
        list_name_1: ListModel(
            name: list_name_1,
            items: [1,2,3],
            primary_person: 1
        )
        list_name_2: ListModel(
            name: list_name_2,
            items: [4,5]
        )
    }
    ```

    serialises to:

    ```
    [
        {
            name: list_name_1,
            items: [1,2,3]
            primary_person: 1
        }
        {
            name: list_name_2,
            items: [4,5]
        }
    ]
    ```
    """

    def __init__(self, existing_items: Optional[List[Mapping]] = None):
        existing_items = existing_items or []

        self._lists = self._build_map(existing_items)

        self._is_dirty = False

    def __getitem__(self, list_name):
        try:
            return self._lists[list_name]
        except KeyError:
            return ListModel(list_name)

    def __delitem__(self, list_name):
        del self._lists[list_name]

    def __repr__(self):
        return f'<ListStore lists={self._lists}>'

    @staticmethod
    def _build_map(list_models: List[Mapping]):
        """ Builds the list_store data structure from a list of dictionaries"""
        return {
            list_model['name']: ListModel(**list_model) for list_model in list_models
        }

    def get(self, item: str):
        return self.__getitem__(item)

    def get(self, item: str):
        return self.__getitem__(item)

    def _generate_identifier(self):
        """ Generate an unused random 6 character string"""
        while True:
            candidate = random_string(EQ_LIST_ITEM_ID_LENGTH)
            if candidate not in self._list_item_ids():
                return candidate

    def _list_item_ids(self):
        ids = []
        for named_list in self._lists.values():
            ids.extend(named_list.items)

        return ids

    @property
    def is_dirty(self):
        return self._is_dirty

    def delete_list_item(self, list_name, item_id):
        try:
            self[list_name].items.remove(item_id)
        except ValueError:
            pass

        if self[list_name].primary_person == item_id:
            self[list_name].primary_person = None

        if not self[list_name].items:
            del self[list_name]

        self._is_dirty = True

    def add_list_item(self, list_name, primary_person=False):
        """ Add a new list item to a named list.

        If the list does not exist, it will be created

        Args:
            list_name: The list to add to or create
            primary_person: Whether the list item represents a primary person

        Returns:
            list item identifier for the new item
        """
        named_list = self._lists.get(list_name, ListModel(list_name))

        list_item_id = self._generate_identifier()

        if primary_person:
            named_list.primary_person = list_item_id
            named_list.items.insert(0, list_item_id)
        else:
            named_list.items.append(list_item_id)

        self._lists[list_name] = named_list
        self._is_dirty = True

        return list_item_id

    def serialise(self):
        return [list_model.serialise() for list_model in self._lists.values()]

    @classmethod
    def deserialise(cls, serialised: list):
        if not serialised:
            return cls()

        return cls(existing_items=serialised)
