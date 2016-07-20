

class Item(object):
    '''
    Abstract class for all items in a schema. Subclasses must provide an id and redefine State accordingly
    '''
    def construct_state(self):
        state_class = self.get_state_class()
        if state_class:
            state = state_class(self.id)
            for child in self.children:
                child_state = child.construct_state()
                state.children.append(child_state)
            return state
        else:
            return None

    def get_state_class(self):
        pass
