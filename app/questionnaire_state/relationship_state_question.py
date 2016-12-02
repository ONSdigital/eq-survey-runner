from app.globals import get_answer_store
from app.jinja_filters import format_household_member_name
from app.questionnaire_state.state_repeating_answer_question import RepeatingAnswerStateQuestion

from flask_login import current_user


class RelationshipStateQuestion(RepeatingAnswerStateQuestion):
    def __init__(self, id, schema_item):
        super().__init__(id=id, schema_item=schema_item)

    def build_repeating_state(self, user_input):
        template_answer = self.answers.pop()
        group_instance = template_answer.group_instance
        first_names = get_answer_store(current_user).filter(answer_id='first-name')
        last_names = get_answer_store(current_user).filter(answer_id='last-name')

        household_answers = list(zip(first_names, last_names))
        remaining_answers = list(zip(first_names[group_instance + 1:], last_names[group_instance + 1:])) \
            if self.group_instance < len(household_answers) else []

        for index, answer in enumerate(remaining_answers):
            for answer_schema in self.schema_item.answers:
                new_answer_state = self.create_new_answer_state(answer_schema, index, group_instance)

                current_person_name = format_household_member_name([
                    household_answers[group_instance][0]['value'],
                    household_answers[group_instance][1]['value'],
                ])
                new_answer_state.schema_item.widget.current_person = current_person_name

                other_person_name = format_household_member_name([
                    answer[0]['value'],
                    answer[1]['value'],
                ])
                new_answer_state.schema_item.widget.other_person = other_person_name
                self.answers.append(new_answer_state)
