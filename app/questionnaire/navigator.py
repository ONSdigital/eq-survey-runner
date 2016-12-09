import copy
import logging

from app.data_model.answer_store import Answer, AnswerStore
from app.helpers.schema_helper import SchemaHelper
from app.questionnaire.location import Location
from app.questionnaire.rules import evaluate_goto, evaluate_repeat

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

        self.first_block_id = SchemaHelper.get_first_block_id(self.survey_json)
        self.first_group_id = SchemaHelper.get_first_group_id(self.survey_json)
        self.last_group_id = SchemaHelper.get_last_group_id(self.survey_json)

        self.first_block_location = Location(self.first_group_id, 0, self.first_block_id)

        self.location_path = self.get_location_path()
        self.first_location = self.location_path[0]

    @staticmethod
    def _block_index_for_location(blocks, location):
        if not location.is_interstitial():
            return next(index for (index, b) in enumerate(blocks) if b["block"]["id"] == location.block_id and
                        b["group_id"] == location.group_id and b['group_instance'] == location.group_instance)
        return None

    def build_path(self, blocks, this_location, path):
        """
        Recursive method which visits all the blocks and returns path taken
        given a list of answers

        :param blocks: A list containing all block content in the survey
        :param this_location: The location to visit, represented as a dict
        :param path: The known path as a list which has been visited already
        :return: A list of block ids followed through the survey
        """
        if this_location.block_id in self.CLOSING_INTERSTITIAL_PATH:
            return path

        path.append(this_location)

        # Return the index of the block id to be visited
        block_index = self._block_index_for_location(blocks, this_location)

        block = blocks[block_index]["block"]

        if 'routing_rules' in block and len(block['routing_rules']) > 0:
            for rule in block['routing_rules']:
                if SchemaHelper.is_goto_rule(rule) and evaluate_goto(rule['goto'], self.metadata, self.answer_store, this_location.group_instance):
                    next_location = copy.copy(this_location)
                    next_location.block_id = rule['goto']['id']

                    next_block_index = self._block_index_for_location(blocks, next_location)

                    # We're jumping backwards, so need to delete current answer
                    if next_block_index is not None and block_index > next_block_index:
                        answer = Answer(answer_id=rule['goto']['when']['id'],
                                        answer_instance=0,
                                        block_id=this_location.block_id,
                                        group_id=this_location.group_id,
                                        group_instance=this_location.group_instance)
                        self.answer_store.remove(answer)

                    return self.build_path(blocks, next_location, path)

        # If this isn't the last block in the set evaluated
        elif block_index != len(blocks) - 1:
            next_location = Location(blocks[block_index + 1]['group_id'],
                                     blocks[block_index + 1]['group_instance'],
                                     blocks[block_index + 1]['block']['id'])

            return self.build_path(blocks, next_location, path)
        return path

    def update_answer_store(self, answer_store):
        """
        Updates the answer store and dependant location_path to the supplied answer_store
        :param answer_store:
        :return:
        """
        self.answer_store = answer_store
        self.location_path = self.get_location_path()

    def get_routing_path(self):
        """
        Returns a list of the block ids visited based on answers provided
        :return: List of block location dicts
        """
        return self.build_path(self.get_blocks(), self.first_block_location, [])

    def can_reach_summary(self, routing_path=None):
        """
        Determines whether the end of a given routing path can be reached given
        a set of answers
        :param routing_path:
        :return:
        """
        blocks = self.get_blocks()
        routing_path = routing_path or self.build_path(blocks, self.first_block_location, [])
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

    def get_location_path(self):
        """
        Returns a list of url locations visited based on answers provided
        :return: List of block location dicts, with preceeding/closing interstitial pages included
        """
        routing_path = self.get_routing_path()
        can_reach_summary = self.can_reach_summary(routing_path)

        # Make sure we don't update original

        location_path = [Location(self.first_group_id, 0, block_id) for block_id in self.preceeding_path]

        location_path += routing_path

        if can_reach_summary:
            for block_id in Navigator.CLOSING_INTERSTITIAL_PATH:
                location_path.append(Location(self.last_group_id, 0, block_id))

        return location_path

    def get_blocks(self):
        blocks = []

        for group_index, group in enumerate(SchemaHelper.get_groups(self.survey_json)):
            no_of_repeats = 1

            for rule in SchemaHelper.get_repeat_rules(group):
                no_of_repeats = evaluate_repeat(rule['repeat'], self.answer_store)

            for i in range(0, no_of_repeats):
                blocks.extend([{
                    "group_id": group['id'],
                    "group_instance": i,
                    "block": block,
                } for block in group['blocks']])
        return blocks

    def _get_current_location_index(self, current_location):
        if current_location in self.location_path:
            return self.location_path.index(current_location)
        return None

    def get_next_location(self, current_location):
        """
        Returns the next 'location' to visit given a set of user answers
        :param current_location:
        :return: The next location as a dict
        """
        current_location_index = self._get_current_location_index(current_location)

        if current_location_index is not None and current_location_index < len(self.location_path) - 1:
            return self.location_path[current_location_index + 1]
        return None

    def get_previous_location(self, current_location):
        """
        Returns the next 'location' to visit given a set of user answers
        :param current_location:
        :return: The previous location as a dict
        """
        current_location_index = self._get_current_location_index(current_location)

        if current_location_index is not None and current_location_index != 0:
            return self.location_path[current_location_index - 1]
        return None

    def get_latest_location(self, completed_blocks=None):
        """
        Returns the latest 'location' based on the location path and previously completed blocks

        :param completed_blocks:
        :return:
        """
        if completed_blocks:
            incomplete_blocks = [item for item in self.location_path if item.__dict__ not in completed_blocks]

            if incomplete_blocks:
                return incomplete_blocks[0]

        return self.first_location
