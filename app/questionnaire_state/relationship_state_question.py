from app.globals import get_answer_store
from app.questionnaire_state.state_repeating_answer_question import RepeatingAnswerStateQuestion

from flask_login import current_user


class RelationshipStateQuestion(RepeatingAnswerStateQuestion):
    def __init__(self, id, schema_item):
        super().__init__(id=id, schema_item=schema_item)

    def build_repeating_state(self, user_input):
        template_answer = self.answers.pop()
        group_instance = template_answer.group_instance
        household_answers = get_answer_store(current_user).filter(answer_id='household-full-name')
        sorted(household_answers, key=lambda household_answer: household_answer['answer_instance'])
        remaining_answers = household_answers[group_instance + 1:] if self.group_instance < len(household_answers) else []

        for index, answer in enumerate(remaining_answers):
            for answer_schema in self.schema_item.answers:
                new_answer_state = self.create_new_answer_state(answer_schema, index, group_instance)
                new_answer_state.schema_item.widget.current_person = household_answers[group_instance]['value']
                new_answer_state.schema_item.widget.other_person = answer['value']
                self.answers.append(new_answer_state)
