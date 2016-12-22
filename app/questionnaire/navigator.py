import copy
import logging

from collections import defaultdict

from app.data_model.answer_store import AnswerStore
from app.helpers.schema_helper import SchemaHelper
from app.questionnaire.location import Location
from app.questionnaire.rules import evaluate_goto, evaluate_repeat, evaluate_skip_condition, is_goto_rule


logger = logging.getLogger(__name__)


class Navigator:
    PRECEEDING_INTERSTITIAL_PATH = ['introduction']
    CLOSING_INTERSTITIAL_PATH = ['summary', 'thank-you']

    def __init__(self, survey_json, metadata=None, answer_store=None):
        self.answer_store = answer_store or AnswerStore()
        self.metadata = metadata or {}
        self.survey_json = survey_json

        self.preceeding_path = []

        if SchemaHelper.has_introduction(self.survey_json):
            self.preceeding_path = self.PRECEEDING_INTERSTITIAL_PATH

    @staticmethod
    def _block_index_for_location(blocks, location):
        try:
            if not location.is_interstitial():
                return next(index for (index, b) in enumerate(blocks) if b["block"]["id"] == location.block_id and
                            b["group_id"] == location.group_id and b['group_instance'] == location.group_instance)
        except StopIteration:
            logger.error("Navigation failure looking for %s", location)
            raise
        return None

    def build_path(self, blocks, this_location):
        """
        Visits all the blocks from a location forwards and returns path
        taken given a list of answers.

        :param blocks: A list containing all block content in the survey
        :param this_location: The location to visit, represented as a dict
        :return: A list of locations followed through the survey
        """
        path = []
        block_index = 0
        blocks_len = len(blocks)

        # Keep going unless we've hit the last block
        while block_index < blocks_len:
            if this_location.block_id in self.CLOSING_INTERSTITIAL_PATH:
                return path

            block_index = Navigator._block_index_for_location(blocks, this_location)
            if block_index is None:
                logger.error('build_path: _block_index_for_location %s is None (invalid location)', this_location)
                return path

            path.append(this_location)
            block = blocks[block_index]["block"]

            # If routing rules exist then a rule must match (i.e. default goto)
            if 'routing_rules' in block and len(block['routing_rules']) > 0:
                original_this_location = copy.copy(this_location)
                for rule in filter(is_goto_rule, block['routing_rules']):
                    should_goto = evaluate_goto(rule['goto'], self.metadata, self.answer_store, this_location.group_instance)

                    if should_goto:
                        next_location = copy.copy(this_location)
                        next_location.block_id = rule['goto']['id']

                        next_block_index = Navigator._block_index_for_location(blocks, next_location)
                        next_precedes_current = next_block_index is not None and next_block_index < block_index

                        if next_precedes_current:
                            self._remove_rule_answers(rule['goto'], this_location)

                        this_location = next_location
                        break

                # If we haven't changed location based on routing rules then we can't progress any further
                if this_location == original_this_location:
                    break

            # No routing rules, so if this isn't the last block, step forward a block
            elif block_index < len(blocks) - 1:
                this_location = Location(blocks[block_index + 1]['group_id'],
                                         blocks[block_index + 1]['group_instance'],
                                         blocks[block_index + 1]['block']['id'])

            # If we've reached last block stop evaluating the path
            else:
                break

        return path

    def _remove_rule_answers(self, goto_rule, location):
        # We're jumping backwards, so need to delete all answers from which
        # route is derived. Need to filter out conditions that don't use answers
        if 'when' in goto_rule.keys():
            for condition in goto_rule['when']:
                if 'meta' not in condition.keys():
                    self.answer_store.remove(answer_id=condition['id'],
                                             answer_instance=0,
                                             location=location)

    def get_routing_path(self, group_id=None, group_instance=0):
        """
        Returns a list of the block ids visited based on answers provided
        :return: List of block location dicts
        """
        if group_id is None:
            group_id = SchemaHelper.get_first_group_id(self.survey_json)

        first_block_in_group = SchemaHelper.get_first_block_id_for_group(self.survey_json, group_id)
        location = Location(group_id, group_instance, first_block_in_group)

        return self.build_path(self.get_blocks(), location)

    def can_reach_summary(self, routing_path):

        """
        Determines whether the end of a given routing path can be reached given
        a set of answers
        :param routing_path:
        :return:
        """
        blocks = self.get_blocks()
        last_routing_block_id = routing_path[-1].block_id
        last_block_id = blocks[-1]['block']['id']

        if last_block_id == last_routing_block_id:
            return True

        routing_block_id_index = next(index for (index, b) in enumerate(blocks) if b['block']["id"] == last_routing_block_id)

        last_routing_block = blocks[routing_block_id_index]['block']

        if 'routing_rules' in last_routing_block:
            for rule in last_routing_block['routing_rules']:
                goto_rule = rule['goto']
                if 'id' in goto_rule.keys() and goto_rule['id'] == 'summary':
                    return evaluate_goto(goto_rule, self.metadata, self.answer_store, 0)
        return False

    def get_location_path(self, group_id=None, group_instance=0):
        """
        Returns a list of url locations visited based on answers provided
        :return: List of block location dicts, with preceeding/closing interstitial pages included
        """
        if group_id is None:
            group_id = SchemaHelper.get_first_group_id(self.survey_json)

        routing_path = self.get_routing_path(group_id, group_instance)
        can_reach_summary = self.can_reach_summary(routing_path)

        location_path = [Location(group_id, 0, block_id) for block_id in self.preceeding_path]

        location_path += routing_path

        if can_reach_summary:
            for block_id in Navigator.CLOSING_INTERSTITIAL_PATH:
                location_path.append(Location(SchemaHelper.get_last_group_id(self.survey_json), 0, block_id))

        return location_path

    def get_blocks(self):
        blocks = []

        for group_index, group in enumerate(SchemaHelper.get_groups(self.survey_json)):
            if 'skip_condition' in group:
                skip = evaluate_skip_condition(group['skip_condition'], self.metadata, self.answer_store)
                if skip:
                    continue

            no_of_repeats = 1
            repeating_rule = SchemaHelper.get_repeating_rule(group)

            if repeating_rule:
                no_of_repeats = evaluate_repeat(repeating_rule, self.answer_store)

            for i in range(0, no_of_repeats):
                blocks.extend([{
                    "group_id": group['id'],
                    "group_instance": i,
                    "block": block,
                } for block in group['blocks']])
        return blocks

    @staticmethod
    def _get_current_location_index(path, current_location):
        if current_location in path:
            return path.index(current_location)
        return None

    def get_next_location(self, current_location):
        """
        Returns the next 'location' to visit given a set of user answers
        :param current_location:
        :return: The next location as a dict
        """
        location_path = self.get_location_path(current_location.group_id, current_location.group_instance)
        current_location_index = Navigator._get_current_location_index(location_path, current_location)

        if current_location_index is not None and current_location_index < len(location_path) - 1:
            return location_path[current_location_index + 1]
        return None

    def get_previous_location(self, current_location):
        """
        Returns the previous 'location' to visit given a set of user answers
        :param current_location:
        :return: The previous location as a dict
        :return:
        """
        location_path = self.get_location_path(current_location.group_id, current_location.group_instance)
        current_location_index = Navigator._get_current_location_index(location_path, current_location)

        if current_location_index is not None and current_location_index != 0:
            return location_path[current_location_index - 1]
        return None

    def get_latest_location(self, completed_blocks=None):
        """
        Returns the latest 'location' based on the location path and previously completed blocks

        :param completed_blocks:
        :return:
        """
        location_path = self.get_location_path()
        if completed_blocks:
            incomplete_blocks = [item for item in location_path if item not in completed_blocks]

            if incomplete_blocks:
                return incomplete_blocks[0]

        return location_path[0]

    def get_front_end_navigation(self, completed_blocks, current_group_id, current_group_instance):
        """
        Returns the frontend navigation based on the completed blocks, group id and group instance

        :param completed_blocks:
        :param group_id:
        :param group_instance:
        :return: navigation
        """

        if 'navigation' not in self.survey_json:
            return None

        navigation = []

        for group in filter(lambda x: 'hide_in_navigation' not in x, self.survey_json['groups']):

            logger.debug("Building frontend navigation for group %s", group)

            repeating_rule = SchemaHelper.get_repeating_rule(group)
            completed_id = group['completed_id'] if 'completed_id' in group else group['blocks'][-1]['id']

            if repeating_rule:
                no_of_repeats = evaluate_repeat(repeating_rule, self.answer_store)

                if repeating_rule['type'] == 'answer_count':
                    link_names = self._generate_link_names(repeating_rule)
                    self._add_repeating_navigation_item(link_names, completed_blocks, completed_id, group, current_group_id,
                                                        current_group_instance, navigation, no_of_repeats)
                elif no_of_repeats > 0:
                    self._add_single_navigation_item(completed_blocks, completed_id, group, current_group_id, navigation)
            else:
                self._add_single_navigation_item(completed_blocks, completed_id, group, current_group_id, navigation)
        return navigation

    def _add_repeating_navigation_item(self, link_names, completed_blocks, completed_id, group, current_group_id,
                                       current_group_instance, navigation, no_of_repeats):
        for i in range(no_of_repeats):
            if link_names:
                navigation.append({
                    'link_name': link_names.get(i),
                    'link_url': Location(group['id'], i, group['blocks'][0]['id']).url(self.metadata),
                    'completed': any(item for item in completed_blocks if item.group_instance == i and
                                     item.block_id == completed_id),
                    'highlight': group['id'] == current_group_id and i == current_group_instance,
                    'repeating': True
                })

    def _add_single_navigation_item(self, completed_blocks, completed_id, group, current_group_id, navigation):
        navigation.append({
            'link_name': group['title'],
            'link_url': Location(group['id'], 0, group['blocks'][0]['id']).url(self.metadata),
            'completed': any(item for item in completed_blocks if item.block_id == completed_id),
            'highlight': (group['id'] != current_group_id and current_group_id in group['highlight_when']
                          if 'highlight_when' in group else False) or group['id'] == current_group_id,
            'repeating': False,
        })

    def _generate_link_names(self, repeating_rule):
        logger.debug("Building frontend hyperlink names for %s", repeating_rule)

        link_names = defaultdict(list)
        if 'navigation_label_answer_ids' in repeating_rule:
            label_answer_ids = repeating_rule['navigation_label_answer_ids']
        else:
            label_answer_ids = [repeating_rule['answer_id']]

        for answer_id in label_answer_ids:
            answers = self.answer_store.filter(answer_id=answer_id)
            for answer in answers:
                if answer['value']:
                    link_names[answer['answer_instance']].append(answer['value'])

        for link_name in link_names:
            link_names[link_name] = " ".join(link_names[link_name])

        return link_names
