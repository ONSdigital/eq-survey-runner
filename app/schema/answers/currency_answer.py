from app.schema.answer import Answer
from app.validation.positive_integer_type_check import PositiveIntegerTypeCheck
from app.schema.widgets.currency_widget import CurrencyWidget
import logging

logger = logging.getLogger(__name__)


class CurrencyAnswer(Answer):
    def __init__(self, answer_id=None):
        super().__init__(answer_id)
        self.type_checkers.append(PositiveIntegerTypeCheck())
        self.widget = CurrencyWidget(self.id)

    def _cast_user_input(self, user_input):
        return int(user_input)
