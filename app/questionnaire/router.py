class Router:

    def __init__(self, schema, routing_path, completeness, current_location=None):
        self._schema = schema
        self._routing_path = routing_path
        self._completeness = completeness
        self._current_location = current_location

    def can_access_location(self):
        """
        Checks whether the current location is valid and accessible.
        :return: boolean
        """
        if self._is_current_location_valid() and not self._get_section_redirect_location() and not self._get_survey_redirect_location():
            return True

        return False

    def get_next_location(self):
        """
        Get the first incomplete block in section/survey if trying to access the section/survey end,
        and the section/survey is incomplete or gets the next default location if the above is false.
        :return: boolean
        """
        return self._get_section_redirect_location() or self._get_survey_redirect_location() or self._get_default_location()

    def _is_current_location_valid(self):
        """
        Checks whether the current location is within the routing path.
        :return: boolean
        """
        return self._current_location in self._routing_path

    def _get_default_location(self):
        """
        Calculates the next location if the current location is invalid
        or if the current location is valid but not accessible.
        :return: Location to direct to.
        """
        next_location = self._routing_path[0]

        if self._completeness.completed_blocks:
            next_location = self._completeness.get_first_incomplete_location_in_survey()
            if not next_location:
                next_location = self._routing_path[-1]

        return next_location

    def _get_section_redirect_location(self):
        """
        Ensure that the user can't access the section summary if the section is not complete.
        :return: Location to direct to if current location is not accessible.
        """
        if not self._is_current_location_valid():
            return None

        section = self._schema.get_section_by_block_id(self._current_location.block_id)
        expected_location = self._completeness.get_first_incomplete_location_in_section(section)
        block = self._schema.get_block(self._current_location.block_id)
        cannot_access_section_summary = self._current_location != expected_location

        if block['type'] == 'SectionSummary' and cannot_access_section_summary:
            return expected_location

    def _get_survey_redirect_location(self):
        """
        Ensure that the user can't access the end of the survey if the survey is not complete.
        :return: Location to direct to if current location is not accessible.
        """
        if not self._is_current_location_valid():
            return None

        expected_location = self._completeness.get_first_incomplete_location_in_survey()
        block = self._schema.get_block(self._current_location.block_id)
        cannot_access_survey_end = self._current_location != expected_location

        if block['type'] in ['Confirmation', 'Summary'] and cannot_access_survey_end:
            return expected_location
