from __future__ import annotations
from typing import Union, Optional, Dict, List
from dataclasses import dataclass, field, asdict


from structlog import get_logger

logger = get_logger()


@dataclass
class Answer:
    answer_id: str
    value: Union[str, int, float, List]
    list_item_id: Optional[str] = field(default=None)

    @classmethod
    def from_dict(cls, answer_dict: Dict) -> Answer:
        return cls(answer_id=answer_dict['answer_id'],
                   value=answer_dict['value'],
                   list_item_id=answer_dict.get('list_item_id'))

    def for_json(self) -> Dict:
        output = self.to_dict()
        if not self.list_item_id:
            del output['list_item_id']
        return output

    def to_dict(self) -> Dict:
        return asdict(self)
