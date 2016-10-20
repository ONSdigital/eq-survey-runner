

class Node(object):
    def __init__(self, item_id):
        # pointers to pages in the doubly linked list
        self.previous = None
        self.next = None
        self.answers = {}
        # item in the schema this node relates to
        self.item_id = item_id

    def __str__(self):
        return self.item_id
