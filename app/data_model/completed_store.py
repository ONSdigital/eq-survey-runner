from typing import List, Mapping

from app.questionnaire.location import Location


class CompletedStore:
    """
    An object that stores and updates references to sections and locations
    that have been completed.
    """

    def __init__(self, completed: Mapping = None) -> None:
        """
        Instantiate a CompletedStore object that tracks completed locations and sections.
        Args:
            completed: A dict containing completed block locations and section ids
        """
        self._is_dirty = False

        if not completed:
            self._locations = []  # type: List[Location]
            self._sections = []  # type: List[str]
            return

        locations = completed.get('locations', {})
        self._locations = [
            Location.from_dict(location_dict=location) for location in locations
        ]

        self._sections = completed.get('sections', [])

    @property
    def is_dirty(self):
        return self._is_dirty

    @property
    def locations(self):
        return self._locations

    @property
    def sections(self):
        return self._sections

    def add_completed_location(self, location):
        if location not in self._locations:
            self._locations.append(location)
            self._is_dirty = True

    def remove_completed_location(self, location):
        if location in self._locations:
            self._locations.remove(location)
            self._is_dirty = True

    def add_completed_section(self, section_id):
        if section_id not in self._sections:
            self._sections.append(section_id)
            self._is_dirty = True

    def remove_completed_section(self, section_id):
        if section_id in self._sections:
            self._sections.remove(section_id)
            self._is_dirty = True

    def serialise(self):
        locations = [location.for_json() for location in self._locations]
        return {'locations': locations, 'sections': self._sections}

    def clear(self) -> None:
        self._locations.clear()
        self._sections.clear()
        self._is_dirty = True
