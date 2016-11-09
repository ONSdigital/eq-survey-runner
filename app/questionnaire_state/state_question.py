from app.questionnaire_state.state_item import StateItem
from app.data_model.answer_store import AnswerStore


class StateQuestion(StateItem):
    def __init__(self, id, schema_item):
        super().__init__(id=id, schema_item=schema_item)
        self.answers = []
        self.children = self.answers

    def remove_answer(self, answer):
        if answer in self.answers:
            self.answers.remove(answer)

        if answer in self.children:
            self.children.remove(answer)

    def update_state(self, user_input):
        if isinstance(user_input, AnswerStore):
            question_answers = user_input.find_by_question(self.id)
            for index, child in enumerate(self.children):
                answer_id_and_value = {}
                answer_instance = list(filter(None, [answer if answer['answer'] == child.id and answer['answer_instance'] == index else None for answer in question_answers]))
                if len(answer_instance) > 0:
                    answer_id_and_value[child.id] = answer_instance[0]['value']

                child.update_state(answer_id_and_value)

        elif self.schema_item.type == 'RepeatingAnswer':
            for child in self.children:
                key = child.id
                key += '' if child.instance == 0 else str(child.instance)
                answer_id_and_value = {
                  child.id: user_input.get(key)
                }
                child.update_state(answer_id_and_value)

        else:
            super(StateQuestion, self).update_state(user_input)
