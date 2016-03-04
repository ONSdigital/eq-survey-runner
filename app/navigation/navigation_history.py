class NavigationHistory(object):
    def get_history(self):
        raise NotImplementedError()

    def add_history_entry(self, location):
        raise NotImplementedError()
