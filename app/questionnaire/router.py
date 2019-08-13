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
        if (
            location.list_item_id
            and location.list_item_id not in self._list_store[location.list_name].items
        ):
            return False

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

        section_key = (location.section_id, location.list_item_id)

        if (
            self._schema.is_hub_enabled()
            and location.block_id == last_block_location.block_id
            and section_key in self._progress_store.completed_section_keys
        ):
            return url_for('.get_questionnaire')

        # If the section is complete and contains a SectionSummary, return the SectionSummary location
        if (
            last_block_type == 'SectionSummary'
            and current_block_type != last_block_type
            and section_key in self._progress_store.completed_section_keys
        ):
            return last_block_location.url()

        if self.is_survey_complete():
            last_section_id = self._schema.get_section_ids()[-1]
            last_block_id = self._schema.get_last_block_id_for_section(last_section_id)

            return Location(section_id=last_section_id, block_id=last_block_id).url()

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
                    section_id=location.section_id,
                    block_id=previous_block['id'],
                    list_item_ids=list_items,
                )
                return relationship_router.get_last_location_url()

            return previous_location.url()

        if self._schema.is_hub_enabled():
            return url_for('questionnaire.get_questionnaire')

        return None

    def get_first_incomplete_location_in_survey(self):
        incomplete_section_keys = self._get_incomplete_section_keys()

        if incomplete_section_keys:
            section_id, list_item_id = incomplete_section_keys[0]

            section_routing_path = path_finder.routing_path(
                section_id=section_id, list_item_id=list_item_id
            )
            location = path_finder.get_first_incomplete_location(section_routing_path)

            if location:
                return location

        last_section_id = self._schema.get_section_ids()[-1]
        last_block_id = self._schema.get_last_block_id_for_section(last_section_id)

        return Location(section_id=last_section_id, block_id=last_block_id)

    def get_first_incomplete_location_for_section(
        self, routing_path, section_id, list_item_id=None
    ):
        section_key = (section_id, list_item_id)

        if section_key in self._progress_store:
            for location in routing_path:
                if location not in self._progress_store.get_completed_locations(
                    section_id=section_id, list_item_id=list_item_id
                ):
                    return location

        return routing_path[0]

    def get_last_complete_location_for_section(
        self, routing_path, section_id, list_item_id=None
    ):
        section_key = (section_id, list_item_id)

        if section_key in self._progress_store:
            for location in routing_path[::-1]:
                if location in self._progress_store.get_completed_locations(
                    section_id=section_id, list_item_id=list_item_id
                ):
                    return location

    def is_survey_complete(self):
        incomplete_section_keys = self._get_incomplete_section_keys()

        if incomplete_section_keys:
            if len(incomplete_section_keys) > 1:
                return False

            section_id = incomplete_section_keys[0][0]
            if self._does_section_only_contain_summary(section_id):
                return True
            return False

        return True

    def _get_allowable_path(self, routing_path):
        """
        The allowable path is the completed path plus the next location
        """
        allowable_path = []

        if routing_path:
            for location in routing_path:
                allowable_path.append(location)

                if location not in self._progress_store.get_completed_locations(
                    section_id=location.section_id, list_item_id=location.list_item_id
                ):
                    return allowable_path

        return allowable_path

    def _get_incomplete_section_keys(self):
        all_section_ids = self._schema.get_section_ids()

        all_section_keys = []
        for section_id in all_section_ids:
            repeating_list = self._schema.get_repeating_list_for_section(section_id)

            if repeating_list:
                for list_item_id in self._list_store[repeating_list].items:
                    section_key = (section_id, list_item_id)
                    all_section_keys.append(section_key)
            else:
                section_key = (section_id, None)
                all_section_keys.append(section_key)

        incomplete_sections_locations = [
            section_key
            for section_key in all_section_keys
            if section_key not in self._progress_store.completed_section_keys
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
