from app.templating.summary.question import Question


class Block:

    def __init__(self, block_schema, group_id, answer_store, metadata, url_for):
        self.id = block_schema['id']
        self.title = block_schema.get('title')
        self.number = block_schema.get('number')
        self.link = self._build_link(block_schema, group_id, metadata, url_for)
        self.questions = self._build_questions(block_schema, answer_store, metadata)

    @staticmethod
    def _build_link(block_schema, group_id, metadata, url_for):
        link = url_for('questionnaire.get_block',
                       eq_id=metadata['eq_id'],
                       form_type=metadata['form_type'],
                       collection_id=metadata['collection_exercise_sid'],
                       group_id=group_id,
                       group_instance=0,
                       block_id=block_schema['id'])

        return link

    @staticmethod
    def _build_questions(block_schema, answer_store, metadata):
        questions = []
        for question_schema in block_schema.get('questions', []):
            question = Question(question_schema, answer_store, metadata)
            if not question.is_skipped:
                questions.append(question)
        return questions
