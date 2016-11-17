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
        self.max_repeats = None

    def construct_state(self):
        reference_answer = len(get_answer_store(current_user).filter(answer_id='household')) - 1
        schema_answers = [schema_answer for schema_answer in self.answers]

        state_class = self.get_state_class()
        question_state = state_class(self.id, self)

        for answer_schema in schema_answers:
            for i in range(reference_answer):
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
