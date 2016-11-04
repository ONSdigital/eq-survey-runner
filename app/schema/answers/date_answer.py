from app.schema.answer import Answer
from app.schema.exceptions import TypeCheckingException
from app.schema.widgets.date_widget import DateWidget
from app.validation.date_type_check import DateTypeCheck


class DateAnswer(Answer):
    def __init__(self, answer_id=None):
        super().__init__(answer_id)
        self.type_checkers.append(DateTypeCheck())
        self.widget = DateWidget(self.id)

    def get_typed_value(self, post_data):

        user_input = self.get_user_input(post_data)

        for checker in self.type_checkers:
            result = checker.validate(user_input)
            if not result.is_valid:
                raise TypeCheckingException(result.errors[0])

        return self._cast_user_input(user_input)

    def get_user_input(self, post_vars):
        return self.widget.get_user_input(post_vars)
