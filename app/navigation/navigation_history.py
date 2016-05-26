from flask_login import current_user
NAV_HISTORY = "history"


class NavigationHistory(object):
    def get_history(self):
        raise NotImplementedError()

    def add_history_entry(self, location):
        raise NotImplementedError()


class FlaskNavigationHistory(NavigationHistory):

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
