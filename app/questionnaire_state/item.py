import logging
from collections import OrderedDict

logger = logging.getLogger(__name__)


class Item(object):
    def __init__(self, id, schema_item):
        self.id = id
        self.parent = None
        self.children = []
        self.is_valid = None
        self.errors = []
        self.schema_item = schema_item
        self.answer_store = {}
        self.skipped = False
        self.display_on_summary = True

    def update_state(self, user_input):
        for child in self.children:
            child.update_state(user_input)

        # once state is updated collect answers
        self.answer_store = self._collect_answers()

    def _collect_answers(self):
        '''
        Collect answers into a dict keyed by id for quick look up
        '''
        answers_as_dict = {}
        answers = self.get_answers()
        for answer in answers:
            answers_as_dict[answer.id] = answer.input
        return answers_as_dict

    def get_answers(self):
        answers = []
        for child in self.children:
            answers.extend(child.get_answers())
        return answers

    def get_errors(self):
        logger.error("Item get errors called")
        # copy the errors into a new list
        errors = OrderedDict()
        if self.errors:
            errors[self.id] = self.errors

        # recursively call the child items to do the same
        for child in self.children:
            errors.update(child.get_errors())
        logger.error("Item errors list is %s", errors)
        return errors
