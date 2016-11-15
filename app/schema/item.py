from app.questionnaire_state.exceptions import StateException


class Item(object):
    '''
    Abstract class for all items in a schema. Subclasses must provide an id and redefine State accordingly
    '''
    def construct_state(self):
        state_class = self.get_state_class()
        if state_class:
            state = state_class(self.id, self)
            for child in self.children:
                child_state = child.construct_state()
                child_state.parent = state
                state.children.append(child_state)
            return state
        else:
            return None

    def get_state_class(self):
        pass

    def validate(self, state):

        if isinstance(state, self.get_state_class()):
            is_valid = True
            for child_state in state.children:
                child_schema = self.questionnaire.get_item_by_id(child_state.id)
                child_valid = child_schema.validate(child_state)

                if child_valid is not None and child_valid is False:
                    is_valid = False
            return is_valid
        else:
            raise StateException('Cannot validate - incorrect state class')
