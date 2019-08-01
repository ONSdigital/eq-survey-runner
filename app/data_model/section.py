from dataclasses import dataclass
from typing import Optional


@dataclass
class Section:
    """
        Store a section in the questionnaire.

        block_id: The id of the block.
        list_item_id: The list_item_id if this section is associated with a list
    """

    section_id: str
    list_item_id: Optional[str] = None

    def __hash__(self):
        return hash(frozenset(self.__dict__.values()))
