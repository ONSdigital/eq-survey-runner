import bleach


class QuestionnaireManager(object):
    def __init__(self, schema, response_store, validator, validation_store, routing_engine, navigator, navigation_history):
        self._schema = schema
        self._response_store = response_store
        self._validator = validator
        self._validation_store = validation_store
        self._routing_engine = routing_engine
        self._navigator = navigator
        self._navigation_history = navigation_history

    def process_incoming_responses(self, post_data):
        # process incoming post data
        user_responses = self._process_incoming_post_data(post_data)

        cleaned_user_responses = {}
        for key, value in user_responses.items():
            cleaned_user_responses[key] = self._clean_input(value)

        # update the response store with data
        for key, value in cleaned_user_responses.items():
            self._response_store.store_response(key, value)

        # run the validator to update the validation_store
        if self._validator.validate(cleaned_user_responses):
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

    def _process_incoming_post_data(self, post_data):
        user_responses = {}
        for key in post_data.keys():
            if key.endswith('-day'):
                # collect the matching -month, and -year fields and return a single response for validation
                response_id = key[0:-4]
                month_key = response_id + '-month'
                year_key = response_id + '-year'

                if month_key not in post_data.keys() or year_key not in post_data.keys():
                    continue

                # We do not validate here, only concatenate the inputs into a single response which is validated elsewhere
                # we concatenate the fields into a date of the format dd/mm/yyyy
                user_responses[response_id] = post_data[key] + '/' + post_data[month_key] + '/' + post_data[year_key]

            elif key.endswith('-month') or key.endswith('-year'):
                # skip theses, they are handled above
                continue
            elif key.startswith('action['):
                # capture the required action
                pass
            else:
                # for now assume it is a valid response id
                user_responses[key] = post_data[key]

        return user_responses

    def _clean_input(self, value):
        return bleach.clean(value)
