class RoutingEngine(object):
    ''' The routing engine will apply any routing rules dependant on where the user is in the schema
    and what answers they have provided.
    '''
    def __init__(self, schema_model):
        self._schema = schema_model

    def get_next(self, current_location):
        # however we're yet to implement routing so always return the current location
        return current_location
