from typing import List, Dict, Tuple

from app.data_model.progress import Progress
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

    def __contains__(self, section_location) -> bool:
        return section_location in self._progress

    @staticmethod
    def _build_map(in_progress_sections: List[Dict]) -> Dict:
        """ Builds the progress_store's data structure from a list of progress dictionaries"""
        return {
            (section['section_id'], section.get('list_item_id')): Progress.from_dict(
                section
            )
            for section in in_progress_sections
        }

    @property
    def is_dirty(self) -> bool:
        return self._is_dirty

    @property
    def completed_section_locations(self) -> List[Tuple[str]]:
        complete_section_locations = []

        for section_location, section_progress in self._progress.items():
            if section_progress.status == CompletionStatus.COMPLETED:
                complete_section_locations.append(section_location)

        return complete_section_locations

    def update_section_status(
        self, section_status: str, section_id, list_item_id=None
    ) -> None:

        section_location = (section_id, list_item_id)
        if section_location in self._progress:
            self._progress[section_location].status = section_status
            self._is_dirty = True

    def get_section_status(self, section_id, list_item_id=None) -> str:
        section_location = (section_id, list_item_id)
        if section_location in self._progress:
            return self._progress[section_location].status

        return CompletionStatus.NOT_STARTED

    def get_completed_locations(self, section_id, list_item_id=None) -> List[Location]:
        section_location = (section_id, list_item_id)
        if section_location in self._progress:
            return self._progress[section_location].locations

        return []

    def add_completed_location(
        self, location: Location, section_id, list_item_id=None
    ) -> None:

        locations = self.get_completed_locations(section_id, list_item_id)

        if location not in locations:
            locations.append(location)

            section_location = (section_id, list_item_id)

            if section_location not in self._progress:
                self._progress[section_location] = Progress(
                    section_id=section_id,
                    list_item_id=list_item_id,
                    locations=locations,
                )
            else:
                self._progress[section_location].locations = locations

            self._is_dirty = True

    def remove_completed_location(
        self, location: Location, section_id, list_item_id=None
    ) -> None:

        section_location = (section_id, list_item_id)
        if (
            section_location in self._progress
            and location in self._progress[section_location].locations
        ):
            self._progress[section_location].locations.remove(location)

            if not self._progress[section_location].locations:
                del self._progress[section_location]

            self._is_dirty = True

    def remove_progress_for_list_item_id(self, list_item_id: str) -> None:
        """Remove progress associated with a particular list_item_id
        This method iterates through all progress.

        *Not efficient.*
        """

        keys_to_delete = []

        for section_location in self._progress:
            if section_location[1] == list_item_id:
                keys_to_delete.append((section_location[0], section_location[1]))

        for key in keys_to_delete:
            del self._progress[key]

            self._is_dirty = True

    def serialise(self) -> List:
        return list(self._progress.values())

    def clear(self) -> None:
        self._progress.clear()
        self._is_dirty = True
