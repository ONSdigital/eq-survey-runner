from app.questionnaire.location import Location


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

    @classmethod
    def is_first_block_id_for_group(cls, survey_json, group_id, block_id):
        group = cls.get_group(survey_json, group_id)
        return group is not None and group['blocks'][0]['id'] == block_id

    @staticmethod
    def get_last_block_id(survey_json):
        return survey_json['groups'][0]['blocks'][-1]['id']

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
    def get_repeat_rule(group):
        if 'routing_rules' in group:
            for rule in group['routing_rules']:
                if 'repeat' in rule.keys():
                    return rule['repeat']

    @staticmethod
    def get_skip_condition(group):
        return group.get('skip_condition')

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
            repeating_rule = cls.get_repeat_rule(group)
            if repeating_rule and repeating_rule['answer_id'] == answer_id:
                yield group

    @classmethod
    def get_first_location(cls, survey_json):
        return Location(
            group_id=cls.get_first_group_id(survey_json),
            group_instance=0,
            block_id=cls.get_first_block_id(survey_json),
        )

    @classmethod
    def get_last_location(cls, survey_json):
        return Location(
            group_id=cls.get_last_group_id(survey_json),
            group_instance=0,
            block_id=cls.get_last_block_id(survey_json),
        )
