from flask_login import current_user
from abc import ABCMeta, abstractmethod
NAV_HISTORY = "history"


class AbstractNavigationHistory(metaclass=ABCMeta):
    @abstractmethod
    def get_history(self):
        raise NotImplementedError()

    @abstractmethod
    def add_history_entry(self, location):
        raise NotImplementedError()


class NavigationHistory(AbstractNavigationHistory):

    def get_history(self):
        data = current_user.get_questionnaire_data()
        if NAV_HISTORY not in data:
            return []
        else:
            return data[NAV_HISTORY]

    def add_history_entry(self, location):
        data = current_user.get_questionnaire_data()
        if NAV_HISTORY not in data:
            history = [location]
            data[NAV_HISTORY] = history
        else:
            data[NAV_HISTORY].append(location)
