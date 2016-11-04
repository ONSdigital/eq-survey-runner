import copy


class SkipCondition(object):
    def __init__(self):
        self.when = None

    def as_dict(self):
        self_copy = copy.deepcopy(self.__dict__)
        self_copy['when'] = self_copy['when'].__dict__ if self.when else None
        return self_copy
