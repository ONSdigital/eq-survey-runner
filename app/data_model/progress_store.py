from typing import List, MutableMapping, Tuple

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

    def __init__(self, in_progress_sections: List[MutableMapping] = None) -> None:
        """
        Instantiate a ProgressStore object that tracks the status of sections and its completed locations
        Args:
            in_progress_sections: A hierarchical dict containing the section status and completed locations
        """
        self._is_dirty = False  # type: bool
        self._progress = self._build_map(
            in_progress_sections or []
        )  # type: MutableMapping

    def __contains__(self, section_key) -> bool:
        return section_key in self._progress

    @staticmethod
    def _build_map(in_progress_sections: List[MutableMapping]) -> MutableMapping:
        """
        Builds the progress_store's data structure from a list of progress dictionaries

        The `section_key` is tuple consisting of `section_id` and the `list_item_id`
        The `section_progress` is a mapping created from the Progress object

        Example structure:
        {
            ('some-section', 'a-list-item-id'): {
                'section_id': 'some-section',
                'status': 'COMPLETED',
                'list_item_id': 'a-list-item-id',
                'locations': [
                    {
                        'section_id': 'some-section',
                        'block_id': 'some-block',
                        'list_name': 'people',
                        'list_item_id': 'a-list-item-id',
                    }
                ],
            }
        }
        """

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
    def completed_section_keys(self) -> List[Tuple[str]]:
        return [
            section_key
            for section_key, section_progress in self._progress.items()
            if section_progress.status == CompletionStatus.COMPLETED
        ]

    def update_section_status(
        self, section_status: str, section_id, list_item_id=None
    ) -> None:

        section_key = (section_id, list_item_id)
        if section_key in self._progress:
            self._progress[section_key].status = section_status
            self._is_dirty = True

    def get_section_status(self, section_id, list_item_id=None) -> str:
        section_key = (section_id, list_item_id)
        if section_key in self._progress:
            return self._progress[section_key].status

        return CompletionStatus.NOT_STARTED

    def get_completed_locations(self, section_id, list_item_id=None) -> List[Location]:
        section_key = (section_id, list_item_id)
        if section_key in self._progress:
            return self._progress[section_key].locations

        return []

    def add_completed_location(self, location: Location) -> None:

        section_id = location.section_id
        list_item_id = location.list_item_id

        locations = self.get_completed_locations(section_id, list_item_id)

        if location not in locations:
            locations.append(location)

            section_key = (section_id, list_item_id)

            if section_key not in self._progress:
                self._progress[section_key] = Progress(
                    section_id=section_id,
                    list_item_id=list_item_id,
                    locations=locations,
                )
            else:
                self._progress[section_key].locations = locations

            self._is_dirty = True

    def remove_completed_location(self, location: Location) -> None:

        section_key = (location.section_id, location.list_item_id)
        if (
            section_key in self._progress
            and location in self._progress[section_key].locations
        ):
            self._progress[section_key].locations.remove(location)

            if not self._progress[section_key].locations:
                del self._progress[section_key]

            self._is_dirty = True

    def remove_progress_for_list_item_id(self, list_item_id: str) -> None:
        """Remove progress associated with a particular list_item_id
        This method iterates through all progress.

        *Not efficient.*
        """

        section_keys_to_delete = [
            (section, section_list_item_id)
            for section, section_list_item_id in self._progress
            if section_list_item_id == list_item_id
        ]

        for section_key in section_keys_to_delete:
            del self._progress[section_key]

            self._is_dirty = True

    def serialise(self) -> List:
        return list(self._progress.values())

    def clear(self) -> None:
        self._progress.clear()
        self._is_dirty = True
