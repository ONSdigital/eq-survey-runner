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
            raise Exception('Cannot validate - incorrect state class')

    # @TODO: Once the rendering pipeline is rafactored, this method is a candidate for removal
    def augment_with_state(self, state):
        if state.id == self.id:
            self.is_valid = state.is_valid
            self.errors = state.errors
            self.warnings = state.warnings
            for child_state in state.children:
                if self.questionnaire.item_exists(child_state.id):
                    child_schema = self.questionnaire.get_item_by_id(child_state.id)
                    child_schema.augment_with_state(child_state)

    def collect_errors(self):
        return self._collect_property('errors')

    def collect_warnings(self):
        return self._collect_property('warnings')

    def _collect_property(self, property_name):
        collection = {}
        for child in self.children:
            child_properties = child._collect_property(property_name)
            collection = {**collection, **child_properties}

        if hasattr(self, property_name):
            value = getattr(self, property_name)
            if value:
                collection[self.id] = [value]
        return collection
