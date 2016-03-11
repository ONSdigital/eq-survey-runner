class QuestionnaireManager(object):
    def __init__(self, schema, response_store, validator, validation_store, routing_engine, navigator, navigation_history):
        self._schema = schema
        self._response_store = response_store
        self._validator = validator
        self._validation_store = response_store
        self._routing_engine = routing_engine
        self._navigator = navigator
        self._navigation_history = navigation_history

    def process_incoming_responses(self, user_responses):
        # update the response store with POST data
        for key, value in user_responses.items():
            self._response_store.store_response(key, value)

        # run the validator to update the validation_store
        self._validator.validate(user_responses)

        print("current_location")
        current_location = self._navigator.get_current_location()
        print(current_location)

        # do any routing
        next_location = self._routing_engine.get_next(current_location)
        print("next_location")
        print(next_location)

        return self._navigator.go_to(next_location)


    def get_rendering_context(self):
        return {
            "validation_results": self._validation_store,
            "user_responses": self._response_store,
            "schema": self._schema
        }
