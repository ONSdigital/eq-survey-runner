from flask_login import current_user

from app import settings
from app.globals import get_answer_store
from app.jinja_filters import format_household_member_name
from app.questionnaire_state.state_repeating_answer_question import RepeatingAnswerStateQuestion


class RelationshipStateQuestion(RepeatingAnswerStateQuestion):
    def __init__(self, item_id, schema_item):
        super().__init__(item_id=item_id, schema_item=schema_item)

    # pylint: disable=too-many-locals
    # TODO refactor this method to make it more readable
    def build_repeating_state(self, user_input):
        template_answer = self.answers.pop()
        group_instance = template_answer.group_instance
        answer_store = get_answer_store(current_user)

        first_name_answers = answer_store.filter(answer_id='first-name', limit=settings.EQ_MAX_NUM_REPEATS)
        last_name_answers = answer_store.filter(answer_id='last-name', limit=settings.EQ_MAX_NUM_REPEATS)

        first_names = [answer['value'] for answer in first_name_answers]
        last_names = [answer['value'] for answer in last_name_answers]

        household_members = []
        for first_name, last_name in zip(first_names, last_names):
            household_members.append({
                'first-name': first_name,
                'last-name': last_name,
            })

        remaining_people = household_members[group_instance + 1:] if self.group_instance < len(household_members) else []

        current_person_name = format_household_member_name([
            household_members[group_instance]['first-name'],
            household_members[group_instance]['last-name'],
        ])

        for index, remaining_person in enumerate(remaining_people):
            for answer_schema in self.schema_item.answers:
                new_answer_state = self.create_new_answer_state(answer_schema, index, group_instance)

                new_answer_state.schema_item.widget.current_person = current_person_name

                other_person_name = format_household_member_name([
                    remaining_person['first-name'],
                    remaining_person['last-name'],
                ])
                new_answer_state.schema_item.widget.other_person = other_person_name
                self.answers.append(new_answer_state)
