
from app.schema.condition import Condition
import logging

logger = logging.getLogger(__name__)


class ConditionalDisplay(object):

    @staticmethod
    def is_skipped(item, questionnaire_manager):
        skipped = False
        if item.skip_condition:
            when = item.skip_condition.when
            if questionnaire_manager:
                logger.error("ConditionalDisplay - when id is %s", when.id)
                logger.error("ConditionalDisplay - when value is %s", when.value)
                logger.error("ConditionalDisplay - when condition is %s", when.condition)
                answer = questionnaire_manager.find_answer(when.id)
                logger.error("ConditionalDisplay - answer is %s", answer)
                if (when.condition == Condition.NOT_EQUALS and when.value != answer) or (when.condition == Condition.EQUALS and when.value == answer):
                        skipped = True
                logger.error("ConditionalDisplay - skipped is %s", skipped)
        return skipped
