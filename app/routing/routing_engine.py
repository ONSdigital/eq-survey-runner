class RoutingEngine(object):
    def __init__(self, schema_model, response_store):
        self._schema = schema_model
        self._response_store = response_store

        # building routing rules

    def get_next(self, current_location):
        raise NotImplementedError()
