class Node(object):
    def __init__(self, item_id, state):
        # pointers to pages in the doubly linked list
        self.previous = None
        self.next = None

        # item in the schema this node relates to
        self.item_id = item_id

        # the state of the node, this is always a Block object
        self.state = state
