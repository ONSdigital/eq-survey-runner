import logging

from app.data_model.answer_store import Answer, AnswerStore
from app.helpers.schema_helper import SchemaHelper
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

    @classmethod
    def is_interstitial_block(cls, block_id):
        return block_id in cls.PRECEEDING_INTERSTITIAL_PATH or block_id in cls.CLOSING_INTERSTITIAL_PATH

    @classmethod
    def _block_index_for_location(cls, blocks, location):
        if not cls.is_interstitial_block(location['block_id']):
            return next(index for (index, b) in enumerate(blocks) if b["block"]["id"] == location['block_id'] and
                        b["group_id"] == location['group_id'] and b['group_instance'] == location['group_instance'])
        return None

    def build_path(self, blocks, this_location, path):
        """
        Recursive method which visits all the blocks and returns path taken
        given a list of answers

        :param blocks: A list containing all blocks in the survey
        :param this_location: The location to visit
        :param path: The known path as a list which has been visited already
        :return: A list of block ids followed through the survey
        """
        if this_location['block_id'] in self.CLOSING_INTERSTITIAL_PATH:
            return path

        path.append(this_location)

        # Return the index of the block id to be visited
        block_index = self._block_index_for_location(blocks, this_location)

        block = blocks[block_index]["block"]

        if 'routing_rules' in block and len(block['routing_rules']) > 0:
            for rule in block['routing_rules']:
                if SchemaHelper.is_goto_rule(rule) and evaluate_goto(rule['goto'], self.metadata, self.answer_store, this_location['group_instance']):
                    is_meta_rule = SchemaHelper.is_goto_meta_rule(rule)
                    next_location = this_location.copy()
                    next_location['block_id'] = rule['goto']['id']

                    next_block_index = self._block_index_for_location(blocks, next_location)

                    # We're jumping backwards, so need to delete current answer
                    if not is_meta_rule and next_block_index is not None and block_index > next_block_index:
                        answer = Answer(answer_id=rule['goto']['when']['id'],
                                        answer_instance=0,
                                        block_id=this_location['block_id'],
                                        group_id=this_location['group_id'],
                                        group_instance=this_location['group_instance'])
                        self.answer_store.remove(answer)

                    return self.build_path(blocks, next_location, path)

        # If this isn't the last block in the set evaluated
        elif block_index != len(blocks) - 1:
            next_location = {
                "block_id": blocks[block_index + 1]['block']['id'],
                "group_id": blocks[block_index + 1]['group_id'],
                "group_instance": blocks[block_index + 1]['group_instance'],
            }

            return self.build_path(blocks, next_location, path)
        return path

    def update_answer_store(self, answer_store):
        """
        Updates the answer store and dependant location_path to the supplied answer_store
        :param answer_store:
        :return:
        """
        self.answer_store = answer_store

    def get_routing_path(self, group_id, group_instance):
        """
        Returns a list of the block ids visited based on answers provided
        :return: List of block location dicts
        """
        first_block_in_group = SchemaHelper.get_group(self.survey_json, group_id)['blocks'][0]['id']
        location = {
            "group_id": group_id,
            "group_instance": group_instance,
            "block_id": first_block_in_group,
        }
        return self.build_path(self.get_blocks(), location, [])

    def can_reach_summary(self, routing_path=None):

        """
        Determines whether the end of a given routing path can be reached given
        a set of answers
        :param routing_path:
        :return:
        """
        blocks = self.get_blocks()
        first_group_id = SchemaHelper.get_first_group_id(self.survey_json)
        first_block_id = SchemaHelper.get_group(self.survey_json, first_group_id)['blocks'][0]['id'],
        first_block_location = {
            "group_id": first_group_id,
            "group_instance": 0,
            "block_id": first_block_id,
        }
        routing_path = routing_path or self.build_path(blocks, first_block_location, [])
        last_routing_block_id = routing_path[-1]['block_id']
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

    def get_location_path(self, group_id=None, group_instance=None):
        """
        Returns a list of url locations visited based on answers provided
        :return: List of block location dicts, with preceeding/closing interstitial pages included
        """
        if group_id is None:
            group_id = SchemaHelper.get_first_group_id(self.survey_json)
        if group_instance is None:
            group_instance = 0

        routing_path = self.get_routing_path(group_id, group_instance)
        can_reach_summary = self.can_reach_summary(routing_path)

        # Make sure we don't update original
        location_path = [{
            "block_id": block_id,
            "group_id": group_id,
            "group_instance": 0,
        } for block_id in self.preceeding_path]

        location_path += routing_path

        if can_reach_summary:
            for block_id in Navigator.CLOSING_INTERSTITIAL_PATH:
                location_path.append({
                    "block_id": block_id,
                    "group_id": SchemaHelper.get_last_group_id(self.survey_json),
                    "group_instance": 0,
                })

        return location_path

    def get_blocks(self):
        blocks = []

        for group_index, group in enumerate(SchemaHelper.get_groups(self.survey_json)):
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
    def _get_current_location_index(path, current_group_id, current_block_id, current_iteration):
        this_block = {
            "block_id": current_block_id,
            "group_id": current_group_id,
            "group_instance": current_iteration,
        }

        if this_block in path:
            return path.index(this_block)
        return None

    def get_next_location(self, current_group_id=None, current_block_id=None, current_iteration=0):
        """
        Returns the next 'location' to visit given a set of user answers
        :param current_group_id:
        :param current_block_id:
        :param current_iteration:
        :return: The next location as a dict
        """
        location_path = self.get_location_path(current_group_id, current_iteration)
        current_location_index = self._get_current_location_index(location_path, current_group_id, current_block_id, current_iteration)

        if current_location_index is not None and current_location_index < len(location_path) - 1:
            return location_path[current_location_index + 1]
        return None

    def get_previous_location(self, current_group_id=None, current_block_id=None, current_iteration=0):
        """
        Returns the next 'location' to visit given a set of user answers
        :param current_group_id:
        :param current_block_id:
        :return: The previous location as a dict
        :return:
        """
        location_path = self.get_location_path(current_group_id, current_iteration)
        current_location_index = self._get_current_location_index(location_path, current_group_id, current_block_id, current_iteration)

        if current_location_index is not None and current_location_index != 0:
            return location_path[current_location_index - 1]
        return None

    def get_latest_location(self, completed_blocks=None):
        """
        Returns the latest 'location' based on the location path and previously completed blocks

        :param completed_blocks:
        :return:
        """
        if completed_blocks:
            incomplete_blocks = [item for item in self.get_location_path() if item not in completed_blocks]

            if incomplete_blocks:
                return incomplete_blocks[0]

        first_location = {
            "group_id": SchemaHelper.get_first_group_id(self.survey_json),
            "group_instance": 0,
            "block_id": SchemaHelper.get_first_block_id(self.survey_json),
        }
        return first_location

    def get_front_end_navigation(self, completed_blocks, group_id, group_instance):
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

        for group in self.survey_json['groups']:

            logger.debug("Building frontend navigation for group %s", group)

            repeating_rule = SchemaHelper.get_repeating_rule(group)

            if 'hide_in_navigation' not in group:

                completed_id = group['completed_id'] if 'completed_id' in group else group['blocks'][-1]['id']

                if repeating_rule:
                    no_of_repeats = evaluate_repeat(repeating_rule, self.answer_store)
                    answer_id = repeating_rule['answer_id']
                    answers = self.answer_store.filter(answer_id=answer_id)

                    for i in range(no_of_repeats):
                        if answers:
                            navigation.append({
                                'link_name': answers[i]['value'],
                                'group_id': group['id'],
                                'instance': i,
                                'block_id': group['blocks'][0]['id'],
                                'completed': any(item for item in completed_blocks if item['group_instance'] == i and
                                                 item["block_id"] == completed_id),
                                'highlight': group['id'] == group_id and i == group_instance,
                                'repeating': True

                            })
                else:
                    navigation.append({
                        'link_name': group['title'],
                        'group_id': group['id'],
                        'instance': 0,
                        'block_id': group['blocks'][0]['id'],
                        'completed': any(item for item in completed_blocks if item["block_id"] == completed_id),
                        'highlight': (group['id'] != group_id and group_id in group['highlight_when']
                                      if 'highlight_when' in group else False) or group['id'] == group_id,
                        'repeating': False,
                    })
        return navigation
