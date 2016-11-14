from datetime import datetime

from app.schema.question import Question


class DateRangeQuestion(Question):
    def __init__(self):
        super().__init__()

    def validate(self, state):
        is_valid = super().validate(state)
        if is_valid:
            state.errors = []
            state.is_valid = True
            from_date = datetime.strptime(state.children[0].value, "%d/%m/%Y")
            to_date = datetime.strptime(state.children[1].value, "%d/%m/%Y")

            if to_date == from_date:
                state.is_valid = False
                state.errors.append(self.questionnaire.get_error_message("INVALID_DATE_RANGE_TO_FROM_SAME", self.id))
                return False

            if to_date < from_date:
                state.is_valid = False
                state.errors.append(self.questionnaire.get_error_message("INVALID_DATE_RANGE_TO_BEFORE_FROM", self.id))
                return False

        return is_valid
