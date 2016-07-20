from app.schema.answer import Answer
from app.validation.date_type_check import DateTypeCheck
from datetime import datetime


class DateAnswer(Answer):
    def __init__(self):
        super().__init__()
        self.type_checkers.append(DateTypeCheck())

    def get_typed_value(self, post_data):
        day = post_data.get(self.id + '-day', '')
        month = post_data.get(self.id + '-month', '')
        year = post_data.get(self.id + '-year', '')

        user_input = year + '/' + month + '/' + day

        for checker in self.type_checkers:
            result = checker.validate(user_input)
            if not result.is_valid:
                raise Exception(result.errors[0])
                return None

        return self._cast_user_input(user_input)

    def _cast_user_input(self, user_input):
        return datetime.strptime(user_input, "%Y/%m/%d")
