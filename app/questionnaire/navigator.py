import logging

from app.data_model.answer_store import AnswerStore
from app.helpers.schema_helper import SchemaHelper

logger = logging.getLogger(__name__)


def evaluate_rule(when, answer_value):
    """
    Determine whether a rule will be satisfied based on a given answer
    :param when:
    :param answer_value:
    :return:
    """
    match_value = when['value']
    condition = when['condition']

    # Evaluate the condition on the routing rule
    if condition == 'equals' and match_value == answer_value:
        return True
    elif condition == 'not equals' and match_value != answer_value:
        return True
    return False


def evaluate_goto(goto_rule, metadata, answers, group_instance):
    """
    Determine whether a goto rule will be satisfied based on a given answer
    :param goto_rule:
    :param metadata
    :param answers:
    :param group_instance:
    :return:
    """
    if 'when' in goto_rule.keys():

        when = goto_rule['when']

        if 'id' in when:
            answer_index = when['id']
            filtered = answers.filter(answer_id=answer_index, group_instance=group_instance)
            if len(filtered) == 1:
                return evaluate_rule(when, filtered[0]['value'])

        elif 'meta' in when:
            key = when['meta']
            value = get_metadata_value(metadata, key)
            return evaluate_rule(when, value)

        return False
    return True


def get_metadata_value(metadata, keys):
    if not _contains_in_dict(metadata, keys):
        return None

    if "." in keys:
        key, rest = keys.split(".", 1)
        return get_metadata_value(metadata[key], rest)
    else:
        return metadata[keys]


def _contains_in_dict(metadata, keys):
    if "." in keys:
        key, rest = keys.split(".", 1)
        if key not in metadata:
            return False
        return _contains_in_dict(metadata[key], rest)
    else:
        return keys in metadata


def evaluate_repeat(repeat_rule, answers):
    """
    Returns the number of times repetition should occur based on answers
    :param repeat_rule:
    :param answers:
    :return: The number of times to repeat
    """
    if 'answer_id' in repeat_rule and 'type' in repeat_rule:
        repeat_index = repeat_rule['answer_id']
        filtered = answers.filter(answer_id=repeat_index)
        if repeat_rule['type'] == 'answer_value':
            if len(filtered) == 1:
                return int(filtered[0]['value'])
            return 1
        elif repeat_rule['type'] == 'answer_count':
            return len(filtered)


class Navigator:
    PRECEEDING_INTERSTITIAL_PATH = ['introduction']
    CLOSING_INTERSTITIAL_PATH = ['summary', 'thank-you']

    def __init__(self, survey_json, metadata=None, answer_store=None):
        self.answer_store = answer_store or AnswerStore()
        self.metadata = metadata or {}
        self.survey_json = survey_json

        self.first_block_id = SchemaHelper.get_first_block_id(self.survey_json)
        self.first_group_id = SchemaHelper.get_first_group_id(self.survey_json)
        self.last_group_id = SchemaHelper.get_last_group_id(self.survey_json)
        self.location_path = self.get_location_path()

    @classmethod
    def is_interstitial_block(cls, block_id):
        return block_id in cls.PRECEEDING_INTERSTITIAL_PATH or block_id in cls.CLOSING_INTERSTITIAL_PATH

    def build_path(self, blocks, group_id, group_instance, block_id, path):
        """
        Recursive method which visits all the blocks and returns path taken
        given a list of answers

        :param blocks: A list containing all blocks in the survey
        :param group_id: The group id to visit
        :param group_instance: The group instance to visit
        :param block_id: The block id to visit
        :param path: The known path as a list which has been visited already
        :return: A list of block ids followed through the survey
        """
        if block_id in self.CLOSING_INTERSTITIAL_PATH:
            return path

        this_block = {
            "block_id": block_id,
            "group_id": group_id,
            "group_instance": group_instance,
        }

        path.append(this_block)

        # Return the index of the block id to be visited
        block_id_index = next(index for (index, b) in enumerate(blocks) if b["block"]["id"] == block_id and
                              b["group_id"] == group_id and b['group_instance'] == group_instance)

        block = blocks[block_id_index]["block"]

        if 'routing_rules' in block and len(block['routing_rules']) > 0:
            for rule in block['routing_rules']:
                is_goto_rule = 'goto' in rule and 'when' in rule['goto'].keys() or 'id' in rule['goto'].keys()
                if is_goto_rule and evaluate_goto(rule['goto'], self.metadata, self.answer_store, group_instance):
                    return self.build_path(blocks, group_id, group_instance, rule['goto']['id'], path)

        # If this isn't the last block in the set evaluated
        elif block_id_index != len(blocks) - 1:
            next_block_id = blocks[block_id_index + 1]['block']['id']
            next_group_id = blocks[block_id_index + 1]['group_id']
            next_group_instance = blocks[block_id_index + 1]['group_instance']

            return self.build_path(blocks, next_group_id, next_group_instance, next_block_id, path)
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
        return self.build_path(self.get_blocks(), self.first_group_id, 0, self.first_block_id, [])

    def can_reach_summary(self, routing_path=None):
        """
        Determines whether the end of a given routing path can be reached given
        a set of answers
        :param routing_path:
        :return:
        """
        blocks = self.get_blocks()
        routing_path = routing_path or self.build_path(blocks, self.first_group_id, 0, self.first_block_id, [])
        last_routing_block_id = routing_path[-1]['block_id']
        last_block_id = blocks[-1]['block']['id']

        if last_block_id == last_routing_block_id:
            return True

        routing_block_id_index = next(
            index for (index, b) in enumerate(blocks) if b['block']["id"] == last_routing_block_id)

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
        location_path = [{
            "block_id": block_id,
            "group_id": self.first_group_id,
            "group_instance": 0,
        } for block_id in Navigator.PRECEEDING_INTERSTITIAL_PATH]

        location_path += routing_path

        if can_reach_summary:
            for block_id in Navigator.CLOSING_INTERSTITIAL_PATH:
                location_path.append({
                    "block_id": block_id,
                    "group_id": self.last_group_id,
                    "group_instance": 0,
                })

        return location_path

    def get_blocks(self):
        blocks = []
        for group_index, group in enumerate(SchemaHelper.get_groups(self.survey_json)):
            blocks.extend([{
                "group_id": group['id'],
                "group_instance": 0,
                "block": block,
            } for block in group['blocks']])

            for rule in SchemaHelper.get_repeat_rules(group):
                no_of_times = evaluate_repeat(rule['repeat'], self.answer_store)
                for i in range(1, no_of_times):
                    blocks.extend([{
                        "group_id": group['id'],
                        "group_instance": i,
                        "block": block,
                    } for block in group['blocks']])
        return blocks

    @classmethod
    def get_first_location(cls):
        return cls.PRECEEDING_INTERSTITIAL_PATH[0]

    def _get_current_location_index(self, current_group_id, current_block_id, current_iteration):
        current_group_id = current_group_id or self.first_group_id

        this_block = {
            "block_id": current_block_id,
            "group_id": current_group_id,
            "group_instance": current_iteration,
        }

        if this_block in self.location_path:
            return self.location_path.index(this_block)
        return None

    def get_next_location(self, current_group_id=None, current_block_id=None, current_iteration=0):
        """
        Returns the next 'location' to visit given a set of user answers
        :param current_group_id:
        :param current_block_id:
        :param current_iteration:
        :return: The next location as a dict
        """
        current_location_index = self._get_current_location_index(current_group_id, current_block_id, current_iteration)

        if current_location_index is not None and current_location_index < len(self.location_path) - 1:
            return self.location_path[current_location_index + 1]
        return None

    def get_previous_location(self, current_group_id=None, current_block_id=None, current_iteration=0):
        """
        Returns the next 'location' to visit given a set of user answers
        :param current_group_id:
        :param current_block_id:
        :return: The previous location as a dict
        :return:
        """
        current_location_index = self._get_current_location_index(current_group_id, current_block_id, current_iteration)

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
            incomplete_blocks = [item for item in self.get_location_path() if item not in completed_blocks]

            if incomplete_blocks:
                return incomplete_blocks[0]

        return {
            'block_id': self.get_first_location(),
            'group_id': SchemaHelper.get_first_group_id(self.survey_json),
            'group_instance': 0,
        }
