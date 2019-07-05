from typing import List, Mapping, MutableMapping

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

    def __init__(self, in_progress_sections: Mapping = None) -> None:
        """
        Instantiate a ProgressStore object that tracks the status of sections and its completed locations
        Args:
            in_progress_sections: A hierarchical dict containing the section status and completed locations
        """
        self._is_dirty = False  # type: bool
        self._progress = {}  # type: MutableMapping

        if not in_progress_sections:
            return

        for section_id, serialised_section in in_progress_sections.items():
            self._progress[section_id] = {
                'status': serialised_section['status'],
                'locations': [
                    Location.from_dict(location_dict=location)
                    for location in serialised_section['locations']
                ],
            }

    def __contains__(self, section_id):
        return section_id in self._progress

    @property
    def is_dirty(self) -> bool:
        return self._is_dirty

    @property
    def completed_section_ids(self) -> List[str]:
        complete_section_ids = []
        for section_id, section_progress in self._progress.items():
            if section_progress['status'] == CompletionStatus.COMPLETED:
                complete_section_ids.append(section_id)

        return complete_section_ids

    def update_section_status(self, section_id: str, section_status: str) -> None:
        if section_id in self._progress:
            self._progress[section_id]['status'] = section_status
            self._is_dirty = True

    def get_section_status(self, section_id: str) -> str:
        if section_id in self._progress:
            return self._progress[section_id]['status']

        return CompletionStatus.NOT_STARTED

    def get_completed_locations(self, section_id: str) -> List[Location]:
        if section_id in self._progress:
            return self._progress[section_id]['locations']

        return []

    def add_completed_location(self, section_id: str, location: Location) -> None:
        locations = self.get_completed_locations(section_id)

        if location not in locations:
            locations.append(location)

            if section_id not in self._progress:
                self._progress[section_id] = {}

            self._progress[section_id]['locations'] = locations
            self._is_dirty = True

    def remove_completed_location(self, section_id: str, location: Location) -> None:
        if (
            section_id in self._progress
            and location in self._progress[section_id]['locations']
        ):
            self._progress[section_id]['locations'].remove(location)

            if not self._progress[section_id]['locations']:
                del self._progress[section_id]

            self._is_dirty = True

    def serialise(self) -> Mapping:
        serialised = {}

        for section_id, section_progress in self._progress.items():
            serialised[section_id] = {
                'status': section_progress['status'],
                'locations': [
                    location.for_json() for location in section_progress['locations']
                ],
            }

        return serialised

    def clear(self) -> None:
        self._progress.clear()
        self._is_dirty = True
