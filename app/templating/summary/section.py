from app.templating.summary.question import Question


class Section:

    def __init__(self, block_id, section_schema, answers):
        self.id = section_schema['id']
        self.title = section_schema['title']
        self.questions = self._build_questions(block_id, section_schema, answers)

    @staticmethod
    def _build_questions(block_id, section_schema, answers):
        questions = []
        for question_schema in section_schema['questions']:
            question = Question(block_id, question_schema, answers)
            if not question.is_skipped(answers):
                questions.append(question)
        return questions
