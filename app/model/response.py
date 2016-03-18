class Response(object):
    def __init__(self):
        self.id = None
        self.label = None
        self.guidance = None
        self.type = None
        self.code = None
        self.container = None
        self.mandatory = None
        self.validation = None

    def get_item_by_id(self, id):
        if id == self.id:
            return self
        else:
            return None
