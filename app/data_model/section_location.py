from dataclasses import dataclass
from typing import Optional

from flask import url_for


@dataclass
class SectionLocation:
    """
        Store a section in the questionnaire.

        section_id: The id of the section
        list_item_id: The list_item_id if this section is associated with a list
    """

    section_id: str
    list_item_id: Optional[str] = None

    def __hash__(self):
        return hash(frozenset(self.__dict__.values()))

    def url(self) -> str:
        """
        Return the survey runner url that this location represents

        :return:
        """
        return url_for(
            'questionnaire.get_section',
            section_id=self.section_id,
            list_item_id=self.list_item_id,
        )
