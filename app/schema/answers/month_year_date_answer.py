from app.schema.answer import Answer
from app.schema.exceptions import TypeCheckingException
from app.schema.widgets.month_year_date_widget import MonthYearDateWidget
from app.validation.month_year_date_type_check import MonthYearDateTypeCheck


class MonthYearDateAnswer(Answer):
    def __init__(self, answer_id=None):
        super().__init__(answer_id)
        self.type_checkers.append(MonthYearDateTypeCheck())
        self.widget = MonthYearDateWidget(self.id)

    def get_typed_value(self, post_data):
        user_input = self.get_user_input(post_data)

        for checker in self.type_checkers:
            result = checker.validate(user_input)
            if not result.is_valid:
                raise TypeCheckingException(result.errors[0])

        return self._cast_user_input(user_input)

    def get_user_input(self, post_vars):
        return self.widget.get_user_input(post_vars)
