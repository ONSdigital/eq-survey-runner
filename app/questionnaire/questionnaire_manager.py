class QuestionnaireManager(object):
    def __init__(self, schema, response_store, validator, validation_store, routing_engine, navigator, navigation_history):
        self._schema = schema
        self._response_store = response_store
        self._validator = validator
        self._validation_store = validation_store
        self._routing_engine = routing_engine
        self._navigator = navigator
        self._navigation_history = navigation_history

    def process_incoming_responses(self, user_responses):

        # update the response store with POST data
        for key, value in user_responses.items():
            self._response_store.store_response(key, value)

        # run the validator to update the validation_store
        if self._validator.validate(user_responses):
            # get the current location in the questionnaire
            current_location = self._navigator.get_current_location()

            # do any routing
            next_location = self._routing_engine.get_next(current_location)

            # go to that location
            self._navigator.go_to(next_location)

        # now return the location
        return self._navigator.get_current_location()

    def get_rendering_context(self):

        # Augment the schema with user responses and validation results

        all_responses = self._response_store.get_responses()
        for item_id, value in all_responses.items():
            item = self._schema.get_item_by_id(item_id)
            if item:
                item.value = value
                validation_result = self._validation_store.get_result(item_id)
                if validation_result:
                    item.is_valid = validation_result.is_valid
                    item.errors = validation_result.get_errors()
                    item.warnings = validation_result.get_warnings()
                else:
                    item.is_valid = None
                    item.errors = None
                    item.warnings = None

        return {
            "validation_results": self._validation_store,
            "user_responses": self._response_store,
            "schema": self._schema
        }
