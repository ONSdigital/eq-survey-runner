from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import MutableMapping, List, Optional, Mapping

from app.questionnaire.location import Location


@dataclass
class Progress:
    section_id: str
    locations: List
    status: Optional[str] = None
    list_item_id: Optional[str] = None

    @classmethod
    def from_dict(cls, progress_dict: Mapping) -> Progress:
        return cls(
            section_id=progress_dict['section_id'],
            locations=[
                Location.from_dict(location_dict=location)
                for location in progress_dict['locations']
            ],
            status=progress_dict['status'],
            list_item_id=progress_dict.get('list_item_id'),
        )

    def for_json(self) -> Mapping:
        locations_for_json = [location.for_json() for location in self.locations]

        output = self.to_dict()
        output['locations'] = locations_for_json

        if not self.list_item_id:
            del output['list_item_id']

        return output

    def to_dict(self) -> MutableMapping:
        return asdict(self)
