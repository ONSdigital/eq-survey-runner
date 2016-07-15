from .navigator import Navigator

from flask_login import current_user
import jsonpickle

NAVIGATION_SESSION_KEY = "nav"


class NavigationStore(object):

    def __init__(self, schema, navigation_history):
        self._schema = schema
        self._navigation_history = navigation_history

    def save_navigator(self, navigator):
        data = current_user.get_questionnaire_data()
        data[NAVIGATION_SESSION_KEY] = jsonpickle.encode(navigator)

    def get_navigator(self):
        data = current_user.get_questionnaire_data()
        if NAVIGATION_SESSION_KEY in data:
            navigator = jsonpickle.decode(data[NAVIGATION_SESSION_KEY])
        else:
            navigator = Navigator(self._schema, self, self._navigation_history)
        return navigator
