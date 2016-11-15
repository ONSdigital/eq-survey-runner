import logging

from app.data_model.answer_store import AnswerStore

logger = logging.getLogger(__name__)


def evaluate_rule(rule, answer_value):
    """
    Determine whether a rule will be satisfied based on a given answer
    :param rule:
    :param answer_value:
    :return:
    """
    when = rule['when']
    match_value = when['value']
    condition = when['condition']

    # Evaluate the condition on the routing rule
    if condition == 'equals' and match_value == answer_value:
        return True
    elif condition == 'not equals' and match_value != answer_value:
        return True
    return False


def evaluate_goto(goto_rule, answers, group_instance):
    """
    Determine whether a goto rule will be satisfied based on a given answer
    :param goto_rule:
    :param answers:
    :param group_instance:
    :return:
    """
    if 'when' in goto_rule.keys():
        answer_index = goto_rule['when']['id']
        filtered = answers.filter(answer_id=answer_index, group_instance=group_instance)
        if len(filtered) == 1:
            answer = filtered[0]
            if evaluate_rule(goto_rule, answer['value']):
                return True
        else:
            return False
    elif 'id' in goto_rule.keys():
        return True
    return None


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

    def __init__(self, survey_json, answer_store=None):
        self.answer_store = answer_store or AnswerStore()
        self.survey_json = survey_json
        self.first_block_id = self.get_first_block_id()
        self.first_group_id = self.get_first_group_id()
        self.last_group_id = self.get_last_group_id()

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
                if 'goto' in rule:
                    should_go = evaluate_goto(rule['goto'], self.answer_store, group_instance)
                    if should_go is True:
                        return self.build_path(blocks, group_id, group_instance, rule['goto']['id'], path)
                    elif should_go is False:
                        return path
        elif block_id_index != len(blocks) - 1:
            next_block_id = blocks[block_id_index + 1]['block']['id']
            next_group_id = blocks[block_id_index + 1]['group_id']
            next_group_instance = blocks[block_id_index + 1]['group_instance']

            return self.build_path(blocks, next_group_id, next_group_instance, next_block_id, path)
        return path

    def get_routing_path(self):
        """
        Returns a list of the block ids visited based on answers provided
        :return: List of block ids
        """
        routing_path = []
        blocks = self.get_blocks()

        return self.build_path(blocks, self.first_group_id, 0, self.first_block_id, routing_path)

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

        if blocks[-1]['block']['id'] == last_routing_block_id:
            return True

        routing_block_id_index = next(index for (index, b) in enumerate(blocks) if b['block']["id"] == last_routing_block_id)

        last_routing_block = blocks[routing_block_id_index]['block']

        if 'routing_rules' in last_routing_block:
            for rule in last_routing_block['routing_rules']:
                goto_rule = rule['goto']
                if 'id' in goto_rule.keys() and goto_rule['id'] == 'summary':
                    return evaluate_goto(goto_rule, self.answer_store, 0)
        return False

    def get_location_path(self):
        """
        Returns a list of url locations visited based on answers provided
        :return:
        """
        blocks = self.get_blocks()
        routing_path = self.build_path(blocks, self.first_group_id, 0, self.first_block_id, [])

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

    def get_first_group_id(self):
        return self.survey_json['groups'][0]['id']

    def get_last_group_id(self):
        return self.survey_json['groups'][-1]['id']

    def get_first_block_id(self):
        return self.survey_json['groups'][0]['blocks'][0]['id']

    def get_blocks(self):
        blocks = []
        for group in self.survey_json['groups']:
            blocks.extend([{
                "group_id": group['id'],
                "group_instance": 0,
                "block": block,
            } for block in group['blocks']])

            if 'routing_rules' in group:
                for rule in group['routing_rules']:
                    if 'repeat' in rule.keys():
                        no_of_times = evaluate_repeat(rule['repeat'], self.answer_store)
                        for i in range(no_of_times - 1):
                            blocks.extend([{
                                "group_id": group['id'],
                                "group_instance": i + 1,
                                "block": block,
                            } for block in group['blocks']])
        return blocks

    @classmethod
    def get_first_location(cls):
        return cls.PRECEEDING_INTERSTITIAL_PATH[0]

    def get_next_location(self, current_group_id=None, current_block_id=None, current_iteration=0):
        """
        Returns the next 'location' to visit given a set of user answers
        :param current_group_id:
        :param current_block_id:
        :param current_iteration:
        :return:
        """
        current_group_id = current_group_id or self.first_group_id
        location_path = self.get_location_path()

        this_block = {
            "block_id": current_block_id,
            "group_id": current_group_id,
            "group_instance": current_iteration,
        }

        if this_block in location_path:

            # Get blocks to be visited
            block_ids = [index for (index, path_item) in enumerate(location_path) if path_item['block_id'] == current_block_id]

            # Return the index of the block id to be visited
            current_location_index = block_ids[current_iteration]

            if current_location_index < len(location_path) - 1:
                return location_path[current_location_index + 1]

    def get_previous_location(self, current_group_id=None, current_block_id=None, current_iteration=0):
        """
        Returns the next 'location' to visit given a set of user answers
        :param current_group_id:
        :param current_block_id:
        :param current_iteration:
        :return:
        """
        current_group_id = current_group_id or self.first_group_id
        location_path = self.get_location_path()

        this_block = {
            "block_id": current_block_id,
            "group_id": current_group_id,
            "group_instance": current_iteration,
        }

        if this_block in location_path:
            # Get blocks to be visited
            block_ids = [index for (index, path_item) in enumerate(location_path) if path_item['block_id'] == current_block_id]

            # Return the index of the block id to be visited
            current_location_index = block_ids[current_iteration]

            if current_location_index != 0:
                return location_path[current_location_index - 1]

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
            'group_id': self.get_first_group_id(),
            'group_instance': 0,
        }
