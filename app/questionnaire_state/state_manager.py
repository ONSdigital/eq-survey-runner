import jsonpickle
from flask_login import current_user


STATE = "state"


class Item(object):

    def __init__(self):
        self.id = None
        self.value = None
        self.type = None
        self.is_valid = None
        self.parent = None
        self.children = []



class QuestionnaireStateManager(object):


    def add_block(self):


    def has_state(self):
        questionnaire_data = current_user.get_questionnaire_data()
        return STATE in questionnaire_data.keys()

    def get_state(self):
        questionnaire_data = current_user.get_questionnaire_data()
        state = questionnaire_data[STATE]
        return jsonpickle.decode(state)

    def save_state(self, questionnaire_state):
        questionnaire_data = current_user.get_questionnaire_data()
        if STATE not in questionnaire_data:
            questionnaire_data[STATE] = jsonpickle.encode(questionnaire_state)
            current_user.save()


questionnaire_state_manager = QuestionnaireStateManager()
