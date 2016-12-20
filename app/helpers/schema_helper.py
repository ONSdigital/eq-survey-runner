class SchemaHelper(object):

    @staticmethod
    def has_introduction(survey_json):
        return 'introduction' in survey_json

    @staticmethod
    def get_first_group_id(survey_json):
        return survey_json['groups'][0]['id']

    @classmethod
    def get_first_block_id_for_group(cls, survey_json, group_id):
        group = cls.get_group(survey_json, group_id)
        if group:
            return group['blocks'][0]['id']

    @staticmethod
    def get_last_group_id(survey_json):
        return survey_json['groups'][-1]['id']

    @staticmethod
    def get_first_block_id(survey_json):
        return survey_json['groups'][0]['blocks'][0]['id']

    @staticmethod
    def get_blocks(survey_json):
        for group in survey_json['groups']:
            for block in group['blocks']:
                yield block

    @staticmethod
    def get_groups(survey_json):
        for group in survey_json['groups']:
            yield group

    @staticmethod
    def get_repeating_rule(group):
        if 'routing_rules' in group:
            for rule in group['routing_rules']:
                if 'repeat' in rule.keys():
                    return rule['repeat']

    @classmethod
    def get_group(cls, survey_json, group_id):
        return next(g for g in cls.get_groups(survey_json) if g["id"] == group_id)

    @classmethod
    def get_block(cls, survey_json, block_id):
        return next(b for b in cls.get_blocks(survey_json) if b["id"] == block_id)

    @classmethod
    def get_answers_that_repeat_in_block(cls, survey_json, block_id):
        block = cls.get_block(survey_json, block_id)
        for section in (s for s in block['sections'] if block['sections']):
            for question in (q for q in section['questions'] if section['questions']):
                if question['type'] == 'RepeatingAnswer':
                    for answer in (a for a in question['answers'] if question['answers']):
                        yield answer

    @classmethod
    def get_groups_that_repeat_with_answer_id(cls, survey_json, answer_id):
        for group in cls.get_groups(survey_json):
            repeating_rule = cls.get_repeating_rule(group)
            if repeating_rule and repeating_rule['answer_id'] == answer_id:
                yield group

    @classmethod
    def get_blocks_that_route_back_to_block(cls, completed_blocks, survey_json, block_id):
        # We're only concerned with blocks completed 'after' the block we're searching for
        if block_id not in [b['block_id'] for b in completed_blocks]:
            return []

        blocks_that_route_back = []
        for completed_block in reversed(completed_blocks):
            block = cls.get_block(survey_json, completed_block['block_id'])

            # Go back through the completed answers until we reach the block we're searching for.
            if block['id'] == block_id:
                break

            if 'routing_rules' in block:
                for routing_rule in block['routing_rules']:
                    if 'goto' in routing_rule and routing_rule['goto']['id'] == block_id:
                        blocks_that_route_back.append(block)
                        break

        return blocks_that_route_back

    @classmethod
    def get_answers_that_route_back_to_block(cls, blocks_that_route_back, survey_json):
        for block_that_routes_back in blocks_that_route_back:
            block = cls.get_block(survey_json, block_that_routes_back['id'])
            for section in (s for s in block['sections'] if block['sections']):
                for question in (q for q in section['questions'] if section['questions']):
                    for answer in (a for a in question['answers'] if question['answers']):
                        yield answer
