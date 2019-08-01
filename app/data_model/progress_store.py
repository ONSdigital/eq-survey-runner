from typing import List, Dict

from app.data_model.progress import Progress
from app.data_model.section import Section
from app.questionnaire.location import Location


class CompletionStatus:
    COMPLETED = 'COMPLETED'
    IN_PROGRESS = 'IN_PROGRESS'
    NOT_STARTED = 'NOT_STARTED'


class ProgressStore:
    """
    An object that stores and updates references to sections and locations
    that have been started.
    """

    def __init__(self, in_progress_sections: List[Dict] = None) -> None:
        """
        Instantiate a ProgressStore object that tracks the status of sections and its completed locations
        Args:
            in_progress_sections: A hierarchical dict containing the section status and completed locations
        """
        self._is_dirty = False  # type: bool
        self._progress = self._build_map(in_progress_sections or [])  # type: Dict

    def __contains__(self, section: Section) -> bool:
        return section in self._progress

    @staticmethod
    def _build_map(in_progress_sections: List[Dict]) -> Dict:
        """ Builds the answer_store's data structure from a list of answer dictionaries"""
        return {
            Section(
                section['section_id'], section.get('list_item_id')
            ): Progress.from_dict(section)
            for section in in_progress_sections
        }

    @property
    def is_dirty(self) -> bool:
        return self._is_dirty

    @property
    def completed_sections(self) -> List[Section]:
        complete_sections = []
        for section, section_progress in self._progress.items():
            if section_progress.status == CompletionStatus.COMPLETED:
                complete_sections.append(section)

        return complete_sections

    def update_section_status(self, section: Section, section_status: str) -> None:
        if section in self._progress:
            self._progress[section].status = section_status
            self._is_dirty = True

    def get_section_status(self, section: Section) -> str:
        if section in self._progress:
            return self._progress[section].status

        return CompletionStatus.NOT_STARTED

    def get_completed_locations(self, section: Section) -> List[Location]:
        if section in self._progress:
            return self._progress[section].locations

        return []

    def add_completed_location(self, section: Section, location: Location) -> None:
        locations = self.get_completed_locations(section)

        if location not in locations:
            locations.append(location)

            if section not in self._progress:
                self._progress[section] = Progress(
                    section_id=section.section_id,
                    list_item_id=section.list_item_id,
                    locations=locations,
                )
            else:
                self._progress[section].locations = locations

            self._is_dirty = True

    def remove_completed_location(self, section: Section, location: Location) -> None:
        if section in self._progress and location in self._progress[section].locations:
            self._progress[section].locations.remove(location)

            if not self._progress[section].locations:
                del self._progress[section]

            self._is_dirty = True

    def remove_progress_for_list_item_id(self, list_item_id: str) -> None:
        """Remove progress associated with a particular list_item_id
        This method iterates through all progress.

        *Not efficient.*
        """

        keys_to_delete = []

        for section in self._progress:
            if section.list_item_id == list_item_id:
                keys_to_delete.append(Section(section.section_id, section.list_item_id))

        for key in keys_to_delete:
            del self._progress[key]

            self._is_dirty = True

    def serialise(self) -> List:
        return list(self._progress.values())

    def clear(self) -> None:
        self._progress.clear()
        self._is_dirty = True
