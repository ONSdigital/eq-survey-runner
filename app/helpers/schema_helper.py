class SchemaHelper(object):

    @staticmethod
    def has_introduction(survey_json):
        return 'introduction' in survey_json

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
    def get_group_blocks(cls, survey_json, group_id):
        group = cls.get_group(survey_json, group_id)

        for block in group['blocks']:
            yield block

    @classmethod
    def get_group(cls, survey_json, group_id):
        return next(g for g in cls.get_groups(survey_json) if g["id"] == group_id)

    @classmethod
    def get_block(cls, survey_json, block_id):
        return next(b for b in cls.get_blocks(survey_json) if b["id"] == block_id)

    @staticmethod
    def is_goto_rule(rule):
        return 'goto' in rule and 'when' in rule['goto'].keys() or 'id' in rule['goto'].keys()

    @staticmethod
    def is_goto_meta_rule(rule):
        return 'goto' in rule and 'when' in rule['goto'].keys() and 'meta' in rule['goto']['when'].keys()
