
class UserJourneyManager(object):
    def __init__(self):
        self.current = None  # the latest page
        self.first = None  # the first page in the doubly linked list
        self.archive = {}  # a dict of completed and discarded

    def
