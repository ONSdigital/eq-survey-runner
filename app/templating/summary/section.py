from app.templating.summary.question import Question


class Section:

    def __init__(self, group_id, group_instance, block_id, section_schema, answers):
        self.id = section_schema['id']
        self.block_id = block_id
        self.group_id = group_id
        self.group_instance = group_instance
        self.title = section_schema['title']
        self.questions = self._build_questions(section_schema, answers)

    @staticmethod
    def _build_questions(section_schema, answers):
        questions = []
        for question_schema in section_schema['questions']:
            question = Question(question_schema, answers)
            if not question.is_skipped(answers):
                questions.append(question)
        return questions
