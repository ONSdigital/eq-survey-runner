class NavigationState(object):
    def __init__(self):
        self.current_position = None

    def to_dict(self):
        return {
            "current_position": self.current_position
        }

    def from_dict(self, values):
        self.current_position = values['current_position'] or None
