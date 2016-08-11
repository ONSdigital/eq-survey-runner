import logging

from app.routing.rules.abstract_rule import AbstractRule


logger = logging.getLogger(__name__)


class GotoBlockRule(AbstractRule):

    def __init__(self, questionnaire_manager, rule):
        super().__init__(questionnaire_manager, rule)

    def next_location(self):

        logger.debug("Processing goto block rule")
        next_location = None
        goto_id = self._rule['goto']['id']

        # If there isn't a 'when' we just go straight to the id
        if 'when' not in self._rule['goto'].keys():
            next_location = goto_id
        else:
            when = self._rule['goto']['when']
            match_value = when['value']
            condition = when['condition']
            user_answer = self._questionnaire_manager.find_answer(when['id'])

            # Evaluate the condition on the routing rule
            if condition == 'equals' and match_value == user_answer:
                next_location = goto_id
            elif condition == 'not equals' and match_value != user_answer:
                next_location = goto_id

        return next_location
