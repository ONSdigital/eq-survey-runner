from app.templating.summary.question import Question


class Section:

    def __init__(self, section_schema, answers_map, link, answers_store, metadata):
        self.id = section_schema['id']
        self.title = section_schema['title']
        self.number = section_schema.get('number', None)
        self.questions = self._build_questions(section_schema, answers_map, answers_store, metadata)
        self.link = link

    @staticmethod
    def _build_questions(section_schema, answers_map, answer_store, metadata):
        questions = []
        for question_schema in section_schema['questions']:
            question = Question(question_schema, answers_map, answer_store, metadata)
            if not question.is_skipped:
                questions.append(question)
        return questions
