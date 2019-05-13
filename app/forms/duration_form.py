from wtforms import Form

from app.forms.custom_fields import CustomIntegerField


class DurationForm(Form):
    def validate(self):
        if all(not field.raw_data[0] for field in self._fields.values()):
            if self.mandatory:
                self._set_error('MANDATORY_DURATION')
                return False

            return True

        if 'years' in self.units and (self.years.data is None or self.years.data < 0):
            self._set_error('INVALID_DURATION')
            return False

        if 'months' in self.units and (
            self.months.data is None or self.months.data < 0
        ):
            self._set_error('INVALID_DURATION')
            return False

        if 'years' in self.units and 'months' in self.units and self.months.data > 11:
            self._set_error('INVALID_DURATION')
            return False

        return True

    def _set_error(self, key):
        list(self._fields.values())[0].errors = [self.answer_errors[key]]

    @property
    def data(self):
        data = super().data
        if all(value is None for value in data.values()):
            return None
        return data


def get_duration_form(answer, error_messages):
    class CustomDurationForm(DurationForm):
        mandatory = answer['mandatory']
        units = answer['units']
        answer_errors = _get_answer_errors(answer, error_messages)

    if 'years' in answer['units']:
        CustomDurationForm.years = CustomIntegerField()

    if 'months' in answer['units']:
        CustomDurationForm.months = CustomIntegerField()

    return CustomDurationForm


def _get_answer_errors(answer, error_messages):
    answer_errors = error_messages.copy()

    if 'validation' in answer and 'messages' in answer['validation']:
        for error_key, error_message in answer['validation']['messages'].items():
            answer_errors[error_key] = error_message

    return answer_errors
