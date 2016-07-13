class Page(object):
    def __init__(self, item_id, page_state):
        # pointers to pages in the doubly linked list
        self.previous_page = None
        self.next_page = None

        # item in the schema this page relates to
        self.item_id = item_id

        self.page_state = page_state
