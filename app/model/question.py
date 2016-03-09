class Question(object):
    def __init__(self):
        self.id = None
        self.title = None
        self.description = None
        self.responses = []
        self.container = None

    def add_response(self, response):
        if response not in self.responses:
            self.responses.append(response)
            response.container = self

    def get_item_by_id(self, id):
        if id == self.id:
            return self
        else:
            item = None
            for response in self.responses:
                candidate = response.get_item_by_id(id)
                if candidate is not None:
                    item = candidate
            return item
