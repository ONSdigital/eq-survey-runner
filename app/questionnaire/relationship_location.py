from __future__ import annotations
from typing import Mapping
from dataclasses import dataclass

from flask import url_for


@dataclass
class RelationshipLocation:
    block_id: str
    from_list_item_id: str
    to_list_item_id: str

    def for_json(self) -> Mapping:
        attributes = vars(self)
        return {k: v for k, v in attributes.items() if v is not None}

    def url(self) -> str:
        return url_for(
            'questionnaire.relationship',
            block_id=self.block_id,
            from_list_item_id=self.from_list_item_id,
            to_list_item_id=self.to_list_item_id,
        )
