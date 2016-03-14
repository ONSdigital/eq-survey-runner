from flask import session
NAV_HISTORY = "history"


class NavigationHistory(object):
    def get_history(self):
        raise NotImplementedError()

    def add_history_entry(self, location):
        raise NotImplementedError()


class FlaskNavigationHistory(NavigationHistory):

    def get_history(self):
        if NAV_HISTORY not in session:
            return []
        else:
            return session[NAV_HISTORY]

    def add_history_entry(self, location):
        if NAV_HISTORY not in session:
            history = [location]
            session[NAV_HISTORY] = history
        else:
            session[NAV_HISTORY].append(location)
        session.permanent = True
