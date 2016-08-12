import logging

from app.repeating_element.repeating_element import RepeatingElement
from app.routing.rules.abstract_rule import AbstractRule

logger = logging.getLogger(__name__)


class RepeatingElementRule(AbstractRule):

    def __init__(self, questionnaire_manager, rule):
        super().__init__(questionnaire_manager, rule)

    def next_location(self):
        logger.debug("Processing repeating block rule")
        next_location = None
        current_block_id = self._questionnaire_manager.get_current_location()
        current_block = self._questionnaire_manager.get_schema_item_by_id(current_block_id)

        # Determine the number of repetition needed
        repetitions = self._questionnaire_manager.find_answer(self._rule['repeat']['answer_id'])

        if current_block.repetition < int(repetitions):
            repeating_manager = RepeatingElement(self._questionnaire_manager)
            next_location = repeating_manager.create_element(current_block)
        elif 'goto' in self._rule['repeat'].keys():
            next_location = self._rule['repeat']['goto']
        # If no extra blocks are needed and there is no goto, default routing will occur
        return next_location
