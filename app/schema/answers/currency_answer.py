import logging

from app.schema.answer import Answer
from app.schema.widgets.currency_widget import CurrencyWidget
from app.validation.positive_integer_type_check import PositiveIntegerTypeCheck

logger = logging.getLogger(__name__)


class CurrencyAnswer(Answer):
    def __init__(self, answer_id=None):
        super().__init__(answer_id)
        self.type_checkers.append(PositiveIntegerTypeCheck())
        self.widget = CurrencyWidget(self.id)

    @staticmethod
    def _cast_user_input(user_input):
        return int(user_input)
