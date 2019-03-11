from flask import url_for

from app.questionnaire.rules import evaluate_when_rules
from app.templating.summary.question import Question


class Block:

    def __init__(self, block_schema, answer_store, metadata, schema):
        self.id = block_schema['id']
        self.title = block_schema.get('title')
        self.number = block_schema.get('number')
        self.link = self._build_link(block_schema['id'])
        self.question = self.get_question(block_schema, answer_store, metadata, schema)

    @staticmethod
    def _build_link(block_id):
        return url_for('questionnaire.get_block',
                       block_id=block_id)

    @staticmethod
    def get_question(block_schema, answer_store, metadata, schema):
        """ Taking question variants into account, return the question which was displayed to the user """
        for variant in block_schema.get('question_variants', []):
            display_variant = evaluate_when_rules(variant.get('when'), schema, metadata, answer_store)
            if display_variant:
                return Question(variant['question'], answer_store, schema).serialize()

        return Question(block_schema['question'], answer_store, schema).serialize()

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'number': self.number,
            'link': self.link,
            'question': self.question,
        }
