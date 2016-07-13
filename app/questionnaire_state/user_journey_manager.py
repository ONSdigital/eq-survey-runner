from app.schema.block import Block as SchemaBlock
from app.questionnaire_state.block import Block as StateBlock
from app.questionnaire_state.page import Page


class UserJourneyManager(object):
    def __init__(self, schema):
        self._schema = schema
        self._current = None  # the latest page
        self._first = None  # the first page in the doubly linked list
        self._archive = []  # a list of completed or discarded pages

    def create_new_state(self, item_id):
        item = self._schema.get_item_by_id(item_id)

        if isinstance(item, SchemaBlock):
            state = StateBlock.construct_state(item)
            page = Page(item_id, state)
            self._append(page)
        else:
            raise TypeError("Can only handle blocks")

    def update_state(self, item_id, user_input):
        item = self._schema.get_item_by_id(item_id)
        if isinstance(item, SchemaBlock):
            if item_id == self._current.id:
                state = self._current.page_state
                state.update_state(user_input)
            else:
                raise ValueError("Updating state for incorrect page")
        else:
            raise TypeError("Can only handle blocks")

    def _append(self, page):
        if not self._first:
            self._first = page
            self._current = page
        else:
            previous_page = self._current
            previous_page.next_page = page
            page.previous_page = previous_page
            self._current = page

    def _truncate(self, page):
        # truncate everything after page and archive it
        while page != self._current:
            self._archive.append(self._pop())
        # finally pop that page
        self._archive.append(self._pop())

    def _pop(self):
        page = self._current
        self._current = page.previous_page
        self._current.next_page = None
        page.previous_page = None
        return page

