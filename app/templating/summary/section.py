from app.templating.summary.question import Question


class Section:

    def __init__(self, section_schema, answers, link):
        self.id = section_schema['id']
        self.title = section_schema['title']
        self.questions = self._build_questions(section_schema, answers)
        self.link = link

    @staticmethod
    def _build_questions(section_schema, answers):
        questions = []
        for question_schema in section_schema['questions']:
            question = Question(question_schema, answers)
            if not question.is_skipped(answers):
                questions.append(question)
        return questions
