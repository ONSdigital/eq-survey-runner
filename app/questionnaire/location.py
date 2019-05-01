from __future__ import annotations
from typing import Optional, Dict
from dataclasses import dataclass

from flask import url_for


@dataclass
class Location:
    """
        Store a location in the questionnaire.

        block_id: The id of the current block. This could be a block inside a list collector
        list_item_id: The list_item_id if this location is associated with a list
        list_name: The list name
    """

    block_id: str
    list_name: Optional[str] = None
    list_item_id: Optional[str] = None

    def __hash__(self):
        return hash(frozenset(self.__dict__.values()))

    @classmethod
    def from_dict(cls, location_dict: Dict):
        block_id = location_dict['block_id']
        list_item_id = location_dict.get('list_item_id')
        list_name = location_dict.get('list_name')
        return cls(block_id, list_name, list_item_id)

    def for_json(self) -> Dict:
        """
        Used to serialise a location to json.
        """
        attributes = vars(self)
        return {k: v for k, v in attributes.items() if v is not None}

    def url(self) -> str:
        """
        Return the survey runner url that this location represents

        :return:
        """
        return url_for('questionnaire.get_block', block_id=self.block_id, list_name=self.list_name, list_item_id=self.list_item_id)
