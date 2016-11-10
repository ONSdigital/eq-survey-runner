class SchemaHelper(object):

    @staticmethod
    def get_first_block_id(survey_json):
        return survey_json['groups'][0]['blocks'][0]['id']

    @staticmethod
    def get_blocks(survey_json):
        blocks = []
        for group in survey_json['groups']:
            blocks.extend([block for block in group['blocks']])
        return blocks

    @classmethod
    def get_block(cls, survey_json, block_id):
        return next(b for b in cls.get_blocks(survey_json) if b["id"] == block_id)
