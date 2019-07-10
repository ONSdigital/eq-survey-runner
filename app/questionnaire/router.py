from flask import url_for

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

        if (
            self._schema.is_hub_enabled()
            and location.block_id == last_block_location.block_id
            and path_finder.is_path_complete(routing_path)
        ):
            return url_for('.get_hub')

        # If the section is complete and contains a SectionSummary, return the SectionSummary location
        if (
            last_block_type == 'SectionSummary'
            and current_block_type != last_block_type
            and path_finder.is_path_complete(routing_path)
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

        block_id = location.block_id

        if self._schema.is_block_list_collector_child(block_id):
            # If this is a list collector sub block, return the collector in the previous link
            block = self._schema.get_block(block_id)
            return Location(block_id=block['parent_id']).url()

        location_index = routing_path.index(location)

        if location_index != 0:
            previous_location = routing_path[location_index - 1]
            previous_block = self._schema.get_block(previous_location.block_id)
            if previous_block['type'] == 'RelationshipCollector':
                list_items = self._list_store.get(previous_block['for_list'])
                relationship_router = RelationshipRouter(
                    previous_block['id'], list_items
                )
                return relationship_router.get_last_location_url()

            return previous_location.url()

        if self._schema.is_hub_enabled():
            return url_for('questionnaire.get_hub')

        return None

    def get_first_incomplete_location_in_survey(self):
        incomplete_section_ids = self._get_incomplete_section_ids()

        if incomplete_section_ids:
            first_incomplete_section = self._schema.get_section(
                incomplete_section_ids[0]
            )
            section_routing_path = path_finder.routing_path(first_incomplete_section)
            location = path_finder.get_first_incomplete_location(section_routing_path)
            if location:
                return location

        all_section_ids = self._schema.get_section_ids()
        last_block_id = self._schema.get_last_block_id_for_section(all_section_ids[-1])
        return Location(block_id=last_block_id)

    def get_first_incomplete_location_for_section(self, section_id, routing_path):
        if section_id in self._progress_store:
            for location in routing_path:
                if location not in self._progress_store.get_completed_locations(
                    section_id
                ):
                    return location
        return routing_path[0]

    def get_last_complete_location_for_section(self, section_id, routing_path):
        if section_id in self._progress_store:
            for location in routing_path[::-1]:
                if location in self._progress_store.get_completed_locations(section_id):
                    return location

    def is_survey_complete(self):
        incomplete_section_ids = self._get_incomplete_section_ids()

        if incomplete_section_ids:
            if len(incomplete_section_ids) > 1:
                return False
            if self._does_section_only_contain_summary(incomplete_section_ids[0]):
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
                if location not in self._progress_store.get_completed_locations(
                    section_id
                ):
                    return allowable_path
        return allowable_path

    def _get_incomplete_section_ids(self):
        all_section_ids = self._schema.get_section_ids()

        incomplete_section_ids = [
            section_id
            for section_id in all_section_ids
            if section_id not in self._progress_store.completed_section_ids
        ]
        return incomplete_section_ids

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
