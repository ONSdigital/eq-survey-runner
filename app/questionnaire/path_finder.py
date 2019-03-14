import copy
from structlog import get_logger

from app.questionnaire.location import Location
from app.questionnaire.routing_path import RoutingPath
from app.questionnaire.rules import (
    evaluate_goto,
    evaluate_skip_conditions,
    is_goto_rule,
)

logger = get_logger()


class PathFinder:

    def __init__(self, schema, answer_store, metadata, completed_blocks):
        self.answer_store = answer_store
        self.metadata = metadata
        self.schema = schema
        self.completed_blocks = completed_blocks
        self._answer_store_hash = self.answer_store.get_hash()
        self._full_routing_path = None

    @staticmethod
    def _block_index_for_location(blocks, location):
        return next((index for (index, block) in enumerate(blocks) if block['id'] == location.block_id), None)

    def build_path(self):
        """
        Visits all the blocks from a location forwards and returns path
        taken given a list of answers.

        :param blocks: A list containing all block content in the survey
        :param this_location: The location to visit, represented as a dict
        :return: A list of locations followed through the survey
        """
        this_location = None

        blocks = []
        path = []
        block_index = 0
        first_groups = self._get_first_group_in_section()

        for group in self.schema.groups:
            if group['id'] in first_groups:
                first_block_in_group = self.schema.get_first_block_id_for_group(group['id'])
                this_location = Location(block_id=first_block_in_group)

            if 'skip_conditions' in group:
                if evaluate_skip_conditions(group['skip_conditions'], self.schema, self.metadata,
                                            self.answer_store, routing_path=path):
                    continue

            blocks.extend(group['blocks'])

            if blocks:
                path, block_index = self._build_path_within_group(blocks, block_index, this_location, path)

        return RoutingPath(path)

    def _get_first_group_in_section(self):
        return [
            section['groups'][0]['id']
            for section in self.schema.sections
        ]

    def _build_path_within_group(self, blocks, block_index, this_location, path):
        # Keep going unless we've hit the last block
        # for block_identifier in blocks:
        while block_index < len(blocks):
            prev_block_index = block_index
            block_index = PathFinder._block_index_for_location(blocks, this_location)
            if block_index is None:
                return path, prev_block_index

            block = blocks[block_index]

            if block.get('skip_conditions') and \
                    evaluate_skip_conditions(block['skip_conditions'], self.schema, self.metadata,
                                             self.answer_store, routing_path=path):

                if block_index == len(blocks) - 1:
                    return path, block_index

                this_location = Location(block_id=blocks[block_index + 1]['id'])
                continue

            if this_location not in path:
                path.append(this_location)

            # If routing rules exist then a rule must match (i.e. default goto)
            if 'routing_rules' in block and block['routing_rules']:
                this_location = self._evaluate_routing_rules(this_location, blocks, block, block_index, path)

                if this_location:
                    continue

            # No routing rules, so if this isn't the last block, step forward a block
            if block_index < len(blocks) - 1:
                this_location = Location(block_id=blocks[block_index + 1]['id'])
                continue

            return path, block_index

    def _evaluate_routing_rules(self, this_location, blocks, block, block_index, path):
        for rule in filter(is_goto_rule, block['routing_rules']):
            should_goto = evaluate_goto(rule['goto'],
                                        self.schema,
                                        self.metadata,
                                        self.answer_store,
                                        routing_path=path)

            if should_goto:
                return self._follow_routing_rule(this_location, rule, blocks, block_index, path)

    def _follow_routing_rule(self, this_location, rule, blocks, block_index, path):
        next_location = copy.copy(this_location)

        if 'group' in rule['goto']:
            next_location.block_id = self.schema.get_first_block_id_for_group(rule['goto']['group'])
        else:
            next_location.block_id = rule['goto']['block']

        next_block_index = PathFinder._block_index_for_location(blocks, next_location)
        next_precedes_current = next_block_index is not None and next_block_index < block_index

        if next_precedes_current:
            self._remove_rule_answers(rule['goto'], this_location)
            path.append(next_location)

        return next_location

    def _remove_rule_answers(self, goto_rule, this_location):
        # We're jumping backwards, so need to delete all answers from which
        # route is derived. Need to filter out conditions that don't use answers
        if 'when' in goto_rule.keys():
            for condition in goto_rule['when']:
                if 'meta' not in condition.keys():
                    self.answer_store.remove(answer_ids=[condition['id']])

        if this_location in self.completed_blocks:
            self.completed_blocks.remove(this_location)

    def get_full_routing_path(self):
        """
        Returns a list of the block ids visited based on answers provided
        :return: List of block location dicts
        """
        latest_answer_store_hash = self.answer_store.get_hash()
        if self._full_routing_path and \
                self._answer_store_hash == latest_answer_store_hash:
            return self._full_routing_path

        self._answer_store_hash = latest_answer_store_hash
        self._full_routing_path = self.build_path()

        return self._full_routing_path

    @staticmethod
    def _get_current_location_index(path, current_location):
        if current_location in path:
            return path.index(current_location)

    def get_next_location(self, current_location):
        """
        Returns the next 'location' to visit given a set of user answers
        If Summary or SectionSummary is available then next location will be those.
        :param current_location:
        :return: The next location as a dict
        """
        routing_path = self.get_full_routing_path()

        current_location_index = PathFinder._get_current_location_index(routing_path, current_location)

        if current_location_index is not None and current_location_index < len(routing_path) - 1:
            if self._is_survey_completed(routing_path):
                return routing_path[-1]     # Go to Summary location

            section_summary_location = self._get_valid_section_summary(current_location.block_id, routing_path)
            if section_summary_location:
                return section_summary_location     # Go to SectionSummary location

            return routing_path[current_location_index + 1]

    def _is_survey_completed(self, routing_path):
        # Check all blocks on routing path are complete
        for location in routing_path[:-1]:  # Don't evaluate end block (Summary or Confirmation)
            if location not in self.completed_blocks:
                return False

        return True

    def _get_valid_section_summary(self, current_block_id, routing_path):
        """
        Check only the section you are on and that all blocks in that section are complete
        If the section has a summary section then pass that back as the next location
        The SectionSummary block itself does not need to be completed
        :param current_block_id: Id of block you're routing from
        :param routing_path: routing path
        :return: location or None
        """
        current_section = self.schema.get_section_by_block_id(current_block_id)

        if self.schema.get_block(current_block_id)['type'] in ['Summary', 'SectionSummary', 'AnswerSummary']:
            return None

        for location in routing_path:
            location_section = self.schema.get_section_by_block_id(location.block_id)
            if location_section == current_section:
                block_type = self.schema.get_block(location.block_id)['type']
                if block_type in ['SectionSummary', 'AnswerSummary']:
                    return location

                if location not in self.completed_blocks:
                    return None

    def get_previous_location(self, current_location):
        """
        Returns the previous 'location' to visit given a set of user answers
        :param current_location:
        :return: The previous location as a dict
        :return:
        """
        group = self.schema.get_group_by_block_id(current_location.block_id)
        first_block_for_group = self.schema.get_first_block_id_for_group(group['id'])

        if first_block_for_group == current_location.block_id:
            return None

        routing_path = self.get_full_routing_path()
        current_location_index = PathFinder._get_current_location_index(routing_path, current_location)

        if current_location_index is not None and current_location_index != 0:
            return routing_path[current_location_index - 1]
