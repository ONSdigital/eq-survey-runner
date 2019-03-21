from flask import url_for

from app.questionnaire.rules import evaluate_skip_conditions
from app.templating.summary.question import Question


class Block:

    def __init__(self, block_schema, answer_store, metadata, schema):
        self.id = block_schema['id']
        self.title = block_schema.get('title')
        self.number = block_schema.get('number')
        self.link = self._build_link(block_schema['id'])
        self.questions = self._build_questions(block_schema, answer_store, metadata, schema)

    @staticmethod
    def _build_link(block_id):
        return url_for('questionnaire.get_block',
                       block_id=block_id)

    @staticmethod
    def _build_questions(block_schema, answer_store, metadata, schema):
        questions = []
        for question_schema in block_schema.get('questions', []):
            is_skipped = evaluate_skip_conditions(question_schema.get('skip_conditions'), schema, metadata, answer_store)
            if not is_skipped:
                question = Question(question_schema, answer_store, metadata, schema).serialize()
                questions.append(question)
        return questions

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'number': self.number,
            'link': self.link,
            'questions': self.questions,
        }
