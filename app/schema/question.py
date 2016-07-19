from app.schema.display import Display
from app.schema.item import Item
from app.questionnaire_state.question import Question as State
from app.schema.questionnaire import QuestionnaireException


class Question(Item):
    def __init__(self):
        self.id = None
        self.title = None
        self.description = ""
        self.answers = []
        self.children = self.answers
        self.container = None
        self.questionnaire = None
        self.validation = None
        self.questionnaire = None
        self.templatable_properties = ['title', 'description']
        self.display = Display()
        self.type = None

    @staticmethod
    def get_instance(question_type):
        # Do imports here to avoid circular dependencies
        from app.schema.questions.general_question import GeneralQuestion
        from app.schema.questions.date_range_question import DateRangeQuestion

        if question_type.upper() == 'GENERAL':
            return GeneralQuestion()
        elif question_type.upper() == 'DATERANGE':
            return DateRangeQuestion()
        else:
            raise QuestionnaireException('Unknown question type "{}"'.format(question_type))

    def add_answer(self, answer):
        if answer not in self.answers:
            self.answers.append(answer)
            answer.container = self

    def get_state_class(self):
        return State
