import logging

from app.schema.condition import Condition

logger = logging.getLogger(__name__)


class ConditionalDisplay(object):

    @staticmethod
    def is_skipped(item, questionnaire_manager):
        skipped = False
        if item.skip_condition:
            when = item.skip_condition.when
            if questionnaire_manager:
                logger.debug("ConditionalDisplay - when id is %s", when.id)
                logger.debug("ConditionalDisplay - when value is %s", when.value)
                logger.debug("ConditionalDisplay - when condition is %s", when.condition)
                answer = questionnaire_manager.find_answer(when.id)
                logger.debug("ConditionalDisplay - answer is %s", answer)
                if (when.condition == Condition.NOT_EQUALS and when.value != answer) or (when.condition == Condition.EQUALS and when.value == answer):
                        skipped = True
                logger.debug("ConditionalDisplay - skipped is %s", skipped)
        return skipped
