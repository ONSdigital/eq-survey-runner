from flask import url_for

from app.data_model.section_location import SectionLocation
from app.helpers.path_finder_helper import path_finder
from app.questionnaire.location import Location
from app.questionnaire.relationship_router import RelationshipRouter


class Router:
    def __init__(self, schema, progress_store=None, list_store=None):
        self._schema = schema
        self._progress_store = progress_store
        self._list_store = list_store

    def can_access_location(self, location: Location, routing_path):
        """
        Checks whether the location is valid and accessible.
        :return: boolean
        """
        allowable_path = self._get_allowable_path(routing_path)

        if location in allowable_path:
            block = self._schema.get_block(location.block_id)
            if (
                block['type'] in ['Confirmation', 'Summary']
                and not self.is_survey_complete()
            ):
                return False

            return True

        return False

    def get_next_location_url(self, location, routing_path):
        """
        Get the first incomplete block in section/survey if trying to access the section/survey end,
        and the section/survey is incomplete or gets the next default location if the above is false.
        """
        current_block_type = self._schema.get_block(location.block_id)['type']
        last_block_location = routing_path[-1]
        last_block_type = self._schema.get_block(last_block_location.block_id)['type']
        section_id = self._schema.get_section_id_for_block_id(location.block_id)
        section_location = SectionLocation(section_id, location.list_item_id)

        if (
            self._schema.is_hub_enabled()
            and location.block_id == last_block_location.block_id
            and section_location in self._progress_store.completed_section_locations
        ):
            return url_for('.get_questionnaire')

        # If the section is complete and contains a SectionSummary, return the SectionSummary location
        if (
            last_block_type == 'SectionSummary'
            and current_block_type != last_block_type
            and section_location in self._progress_store.completed_section_locations
        ):
            return last_block_location.url()

        if self.is_survey_complete():
            section_ids = self._schema.get_section_ids()
            last_block_id = self._schema.get_last_block_id_for_section(section_ids[-1])
            return Location(block_id=last_block_id).url()

        location_index = routing_path.index(location)
        # At end of routing path, so go to next incomplete location
        if location_index == len(routing_path) - 1:
            return self.get_first_incomplete_location_in_survey().url()

        next_location = routing_path[location_index + 1]
        return next_location.url()

    def get_previous_location_url(self, location, routing_path):
        """
        Returns the previous 'location' to visit given a set of user answers
        """
        location_index = routing_path.index(location)

        if location_index != 0:
            previous_location = routing_path[location_index - 1]
            previous_block = self._schema.get_block(previous_location.block_id)
            if previous_block['type'] == 'RelationshipCollector':
                list_items = self._list_store.get(previous_block['for_list']).items
                relationship_router = RelationshipRouter(
                    previous_block['id'], list_items
                )
                return relationship_router.get_last_location_url()

            return previous_location.url()

        if self._schema.is_hub_enabled():
            return url_for('questionnaire.get_questionnaire')

        return None

    def get_first_incomplete_location_in_survey(self):
        incomplete_section_locations = self._get_incomplete_section_locations()

        if incomplete_section_locations:
            section_routing_path = path_finder.routing_path(
                incomplete_section_locations[0]
            )
            location = path_finder.get_first_incomplete_location(section_routing_path)

            if location:
                return location

        all_section_ids = self._schema.get_section_ids()
        last_block_id = self._schema.get_last_block_id_for_section(all_section_ids[-1])

        return Location(block_id=last_block_id)

    def get_first_incomplete_location_for_section(self, section_location, routing_path):
        if section_location in self._progress_store:
            for location in routing_path:
                if location not in self._progress_store.get_completed_locations(
                    section_location
                ):
                    return location

        return routing_path[0]

    def get_last_complete_location_for_section(self, section_location, routing_path):
        if section_location in self._progress_store:
            for location in routing_path[::-1]:
                if location in self._progress_store.get_completed_locations(
                    section_location
                ):
                    return location

    def is_survey_complete(self):
        incomplete_section_locations = self._get_incomplete_section_locations()

        if incomplete_section_locations:
            if len(incomplete_section_locations) > 1:
                return False
            if self._does_section_only_contain_summary(
                incomplete_section_locations[0].section_id
            ):
                return True
            return False

        return True

    def _get_allowable_path(self, routing_path):
        """
        The allowable path is the completed path plus the next location
        """
        allowable_path = []

        if routing_path:
            first_location = routing_path[0]
            section_id = self._schema.get_section_id_for_block_id(
                first_location.block_id
            )

            for location in routing_path:
                allowable_path.append(location)
                section_location = SectionLocation(section_id, location.list_item_id)

                if location not in self._progress_store.get_completed_locations(
                    section_location
                ):
                    return allowable_path

        return allowable_path

    def _get_incomplete_section_locations(self):
        all_section_ids = self._schema.get_section_ids()

        all_section_locations = []
        for section_id in all_section_ids:
            for_list = self._schema.get_repeating_list_for_section(section_id)

            if for_list:
                for list_item_id in self._list_store[for_list].items:
                    section_location = SectionLocation(section_id, list_item_id)
                    all_section_locations.append(section_location)
            else:
                section_location = SectionLocation(section_id)
                all_section_locations.append(section_location)

        incomplete_sections_locations = [
            section_location
            for section_location in all_section_locations
            if section_location not in self._progress_store.completed_section_locations
        ]

        return incomplete_sections_locations

    # This is horrible and only necessary as currently a section can be defined that only
    # contains a Summary or Confirmation. The ideal solution is to move Summary/Confirmation
    # blocks from sections and into the top level of the schema. Once that's done this can be
    # removed.
    def _does_section_only_contain_summary(self, section_id):
        section = self._schema.get_section(section_id)
        groups = section.get('groups')
        if len(groups) == 1:
            blocks = groups[0].get('blocks')
            if len(blocks) == 1:
                block_type = blocks[0].get('type')
                if block_type in ['Summary', 'Confirmation']:
                    return True
        return False
