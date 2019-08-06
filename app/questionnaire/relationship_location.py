from __future__ import annotations
from typing import Mapping, Optional
from dataclasses import dataclass

from flask import url_for


@dataclass
class RelationshipLocation:
    block_id: str
    list_item_id: str
    to_list_item_id: str
    section_id: Optional[str] = None

    def for_json(self) -> Mapping:
        attributes = vars(self)
        return {k: v for k, v in attributes.items() if v is not None}

    def url(self) -> str:
        return url_for(
            'questionnaire.relationship',
            block_id=self.block_id,
            list_item_id=self.list_item_id,
            to_list_item_id=self.to_list_item_id,
        )
