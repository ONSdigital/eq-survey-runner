class SchemaHelper(object):

    @staticmethod
    def get_first_group_id(survey_json):
        return survey_json['groups'][0]['id']

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
    def get_repeat_rules(group):
        if 'routing_rules' in group:
            for rule in group['routing_rules']:
                if 'repeat' in rule.keys():
                    yield rule

    @classmethod
    def get_group(cls, survey_json, group_id):
        return next(g for g in cls.get_groups(survey_json) if g["id"] == group_id)

    @classmethod
    def get_block(cls, survey_json, block_id):
        return next(b for b in cls.get_blocks(survey_json) if b["id"] == block_id)

    @classmethod
    def find_block_with_answer_id(cls, survey_json, answer_id):
        for block in cls.get_blocks(survey_json):
            for section in (s for s in block['sections'] if block['sections']):
                for question in (q for q in section['questions'] if section['questions']):
                    for answer in (a for a in question['answers'] if question['answers']):
                        if answer['id'] == answer_id:
                            return block['id']
        return None

    @classmethod
    def find_groups_with_repeat_for_block_id(cls, survey_json, block_id):
        for group in cls.get_groups(survey_json):
            for rule in cls.get_repeat_rules(survey_json, group):
                answer_id = rule['repeat']['answer_id']
                block_id_for_answer = cls.find_block_with_answer_id(survey_json, answer_id)
                if block_id_for_answer is not None and block_id_for_answer == block_id:
                    yield group['id']
