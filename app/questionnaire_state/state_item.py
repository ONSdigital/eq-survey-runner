import logging

from collections import OrderedDict

from app.questionnaire.rules import evaluate_rule, get_metadata_value

logger = logging.getLogger(__name__)


class StateItem(object):
    def __init__(self, id, schema_item):
        self.id = id
        self.parent = None
        self.children = []
        self.is_valid = None
        self.errors = []
        self.schema_item = schema_item
        self.skipped = False
        self.display_on_summary = True
        self.answer_instance = 0
        self.group_instance = 0

    def update_state(self, user_input):
        for child in self.children:
            child.update_state(user_input)

    def get_answers(self):
        answers = []
        for child in self.children:
            answers.extend(child.get_answers())
        return answers

    def get_errors(self):
        logger.debug("Item get errors called")
        # copy the errors into a new list
        errors = OrderedDict()
        if self.errors:
            errors[self.id] = self.errors

        # recursively call the child items to do the same
        for child in self.children:
            errors.update(child.get_errors())

        logger.debug("Item errors list is %s", errors)
        return errors

    def set_skipped(self, answers, metadata):
        # Process any conditional display rules
        if self.schema_item:

            if hasattr(self.schema_item, 'skip_condition') and self.schema_item.skip_condition:
                rule = self.schema_item.skip_condition
                all_conditions_met = True
                for when in rule['when']:
                    value = answers.get(when['id']) if 'id' in when else get_metadata_value(metadata, when['meta'])
                    if not evaluate_rule(when, value):
                        all_conditions_met = False
                        break

                self.skipped = all_conditions_met

            for child in self.children:
                child.set_skipped(answers, metadata)

    def find_state_item(self, schema_item):
        for child in self.children:
            if child.schema_item == schema_item:
                return child
            else:
                return child.find_state_item(schema_item)

        return None
