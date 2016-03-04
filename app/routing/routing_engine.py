class RoutingEngine(object):
    def __init__(self, schema_model, response_store):
        # building routing rules
        raise NotImplementedError()

    def get_next(self, current_location):
        raise NotImplementedError()
