class Router:

    _first_incomplete_block_in_section = None
    _first_incomplete_block_in_survey = None
    _section = None
    _block = None

    def __init__(self, current_location, routing_path, completness):
        self.current_location = current_location
        self.routing_path = routing_path
        self.completness = completness

    def is_valid_location(self):
        return self.current_location in self.routing_path

    def can_access_location(self, section, block):
        self._section = section
        self._block = block

        is_skipping_to_end_of_section = self._get_first_incomplete_block_in_section()
        if is_skipping_to_end_of_section:
            return False

        self._block = block
        is_skipping_to_end_of_survey = self._get_first_incomplete_block_in_survey()
        if is_skipping_to_end_of_survey:
            return False

        return True

    def get_next_location(self):
        if not self.is_valid_location():
            next_location = self.completness.get_latest_location()
            return next_location

        return self._first_incomplete_block_in_section or self._first_incomplete_block_in_survey

    def _get_first_incomplete_block_in_section(self):
        latest_location = self.completness.get_first_incomplete_location_in_section(self._section)

        if self._block['type'] == 'SectionSummary' and self.current_location != latest_location:
            self._first_incomplete_block_in_section = latest_location

        return self._first_incomplete_block_in_section

    def _get_first_incomplete_block_in_survey(self):
        latest_location = self.completness.get_first_incomplete_location_in_survey()

        if self._block['type'] in ['Confirmation', 'Summary'] and self.current_location != latest_location:
            self._first_incomplete_block_in_survey = latest_location

        return self._first_incomplete_block_in_survey
