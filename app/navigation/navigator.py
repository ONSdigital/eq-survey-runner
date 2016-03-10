from abc import ABCMeta, abstractmethod


class Navigator(object):
    def __init__(self, schema, navigation_history):
        self._schema = schema
        self._navigation_history = navigation_history
        self._store = NavigationStore()

    # destination  "group:block:section:question:<repetition>"
    def _valid_destination(self, destination):
        raise NotImplementedError()

    def get_current_location(self):
        raise NotImplementedError()

    def go_to(self, location):
        raise NotImplementedError()


class NavigationState(object):
    def __init__(self):
        self.started = False
        self.current_position = None
        self.completed = False


class INavigationStore(metaclass=ABCMeta):
    @abstractmethod
    def store_state(self, state):
        pass

    @abstractmethod
    def get_state(self):
        pass


class NavigationStore(INavigationStore):
    def store_state(self, state):
        session["navigation"] = json.dumps(state)
        session.permanent = True

    def get_state(self):
        state = session["navigation"]
        if state:
            return json.loads(state)
        else:
            return NavigationState()
