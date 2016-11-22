import copy

from flask_login import current_user

from app.globals import get_answer_store
from app.schema.question import Question


class HouseholdRelationshipQuestion(Question):
    """
    A Question type that supports repeating answers.
    """
    def __init__(self):
        super().__init__()

    def construct_state(self):
        number_in_household = len(get_answer_store(current_user).filter(answer_id='household')) - 1
        number_answered = len(get_answer_store(current_user).filter(answer_id='relationship', answer_instance=0))
        number_to_answer = number_in_household - number_answered
        schema_answers = [schema_answer for schema_answer in self.answers]
        state_class = self.get_state_class()
        question_state = state_class(self.id, self)

        for answer_schema in schema_answers:
            for i in range(number_to_answer):
                answer_state = answer_schema.construct_state()
                answer_state.parent = question_state
                answer_state.instance = i

                new_answer_schema = copy.deepcopy(answer_schema)
                if i > 0:
                    new_answer_schema.widget.name += '_' + str(i)
                    new_answer_schema.id += '_' + str(i)

                answer_state.schema_item = new_answer_schema
                question_state.children.append(answer_state)

        return question_state
