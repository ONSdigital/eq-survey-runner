import logging

logger = logging.getLogger(__name__)


def evaluate_rule(rule, answer):
    """
    Determine whether a rule will be satisfied based on a given answer
    :param rule:
    :param answer:
    :return:
    """
    when = rule['when']
    match_value = when['value']
    condition = when['condition']

    # Evaluate the condition on the routing rule
    if condition == 'equals' and match_value == answer:
        return True
    elif condition == 'not equals' and match_value != answer:
        return True
    return False


def build_path(blocks, block_id, answers, path):
    """
    Recursive method which visits all the blocks and returns path taken
    given a list of answers

    :param blocks: A list containing all blocks in the survey
    :param block_id: The block id to visit
    :param answers: The answers to use on evaluating rules
    :param path: The known path as a list which has been visited already
    :return: A list of block ids followed through the survey
    """
    if block_id in Navigator.CLOSING_INTERSTITIAL_PATH:
        return path

    path.append(block_id)
    # Return the index of the block id to be visited
    block_id_index = next(index for (index, b) in enumerate(blocks) if b["id"] == block_id)

    if 'routing_rules' in blocks[block_id_index] and len(blocks[block_id_index]['routing_rules']) > 0:
        for rule in blocks[block_id_index]['routing_rules']:
            goto_rule = rule['goto']
            if 'when' in goto_rule.keys():
                answer_index = goto_rule['when']['id']
                if answer_index in answers:
                    answer = answers[answer_index]
                    if evaluate_rule(goto_rule, answer):
                        return build_path(blocks, goto_rule['id'], answers, path)
                else:
                    return path
            elif 'id' in goto_rule.keys():
                return build_path(blocks, goto_rule['id'], answers, path)
    elif block_id_index != len(blocks) - 1:
        next_block_id = blocks[block_id_index + 1]['id']
        return build_path(blocks, next_block_id, answers, path)
    return path


class Navigator:
    PRECEEDING_INTERSTITIAL_PATH = ['introduction']
    CLOSING_INTERSTITIAL_PATH = ['summary', 'thank-you']

    def __init__(self, survey_json):
        self.survey_json = survey_json
        self.blocks = self.get_blocks()
        self.first_block_id = self.blocks[0]['id']

    def get_routing_path(self, answers=None):
        """
        Returns a list of the block ids visited based on answers provided
        :return: List of block ids
        """
        answers = answers or {}
        routing_path = []

        return build_path(self.blocks, self.first_block_id, answers, routing_path)

    def can_reach_summary(self, answers=None, routing_path=None):
        """
        Determines whether the end of a given routing path can be reached given
        a set of answers
        :param routing_path:
        :param answers:
        :return:
        """
        answers = answers or {}
        routing_path = routing_path or build_path(self.blocks, self.first_block_id, answers, [])
        last_routing_block_id = routing_path[-1]

        if self.blocks[-1]['id'] == last_routing_block_id:
            return True

        routing_block_id_index = next(index for (index, b) in enumerate(self.blocks) if b["id"] == last_routing_block_id)

        last_routing_block = self.blocks[routing_block_id_index]

        if 'routing_rules' in last_routing_block:
            for rule in last_routing_block['routing_rules']:
                goto_rule = rule['goto']
                if 'id' in goto_rule.keys() and goto_rule['id'] == 'summary':
                    if 'when' in goto_rule.keys():
                        answer_index = goto_rule['when']['id']
                        if answer_index in answers:
                            answer = answers[answer_index]
                            if evaluate_rule(goto_rule, answer):
                                return True
                    else:
                        return True
        return False

    def get_location_path(self, answers=None):
        """
        Returns a list of url locations visited based on answers provided
        :param answers:
        :return:
        """
        answers = answers or {}
        routing_path = build_path(self.blocks, self.first_block_id, answers, [])

        can_reach_summary = self.can_reach_summary(answers, routing_path)

        # Make sure we don't update original
        location_path = list(Navigator.PRECEEDING_INTERSTITIAL_PATH)
        location_path.extend(routing_path)

        if can_reach_summary:
            location_path.extend(Navigator.CLOSING_INTERSTITIAL_PATH)

        return location_path

    def get_first_block_id(self):
        return self.survey_json['groups'][0]['blocks'][0]['id']

    def get_blocks(self):
        blocks = []
        for group in self.survey_json['groups']:
            blocks.extend([block for block in group['blocks']])
        return blocks

    def get_first_location(self):
        return Navigator.PRECEEDING_INTERSTITIAL_PATH[0]

    def get_next_location(self, answers=None, current_location_id=None):
        """
        Returns the next 'location' to visit given a set of user answers
        :param answers:
        :param current_location_id:
        :return:
        """
        answers = answers or {}
        location_path = self.get_location_path(answers)
        if current_location_id in location_path:
            current_location_index = location_path.index(current_location_id)

            if current_location_index < len(location_path) - 1:
                return location_path[current_location_index + 1]

    def get_previous_location(self, answers=None, current_location_id=None):
        """
        Returns the next 'location' to visit given a set of user answers
        :param answers:
        :param current_location_id:
        :return:
        """
        answers = answers or {}
        location_path = self.get_location_path(answers)
        if current_location_id in location_path:
            current_location_index = location_path.index(current_location_id)

            if current_location_index != 0:
                return location_path[current_location_index - 1]

    def get_latest_location(self, answers=None, completed_blocks=None):
        """
        Returns the latest 'location' based on the location path and previously completed blocks
        :param answers:
        :param completed_blocks:
        :return:
        """
        latest_location = self.get_first_location()

        if completed_blocks:
            answers = answers or {}
            incomplete_blocks = [item for item in self.get_location_path(answers) if item not in completed_blocks]

            if incomplete_blocks:
                latest_location = incomplete_blocks[0]

        return latest_location
