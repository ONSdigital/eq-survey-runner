from app.questionnaire_state.state_repeating_answer_question import RepeatingAnswerStateQuestion
from app.schema.question import Question


class RepeatingAnswerQuestion(Question):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_state_class():
        return RepeatingAnswerStateQuestion
