from app.validation.validators import TimeInputRequired, TimeInputCheck, OptionalForm
from app.forms.custom_integer_field import CustomIntegerField
from wtforms import Form

def get_time_input_form(answer, error_messages):

    class TimeInputForm(Form):
        hour = CustomIntegerField()
        minute = CustomIntegerField()

    validate_with = [OptionalForm()]

    if not error_messages:
        time_input_messages = {}
    else:
        time_input_messages = error_messages.copy()

    if answer['mandatory'] is True:
        if 'validation' in answer and 'messages' in answer['validation'] \
                and 'MANDATORY' in answer['validation']['messages']:
            time_input_messages['MANDATORY'] = answer['validation']['messages']['MANDATORY']

        validate_with = [TimeInputRequired(message=time_input_messages['MANDATORY'])]

    if 'validation' in answer and 'messages' in answer['validation']:
            if 'INVALID_MINUTES' in answer['validation']['messages']:
                time_input_messages['INVALID_MINUTES'] = answer['validation']['messages']['INVALID_MINUTES']
            if 'INVALID_HOURS' in answer['validation']['messages']:
                time_input_messages['INVALID_HOURS'] = answer['validation']['messages']['INVALID_HOURS']

    validate_with += [TimeInputCheck(time_input_messages)]

    TimeInputForm.hour = CustomIntegerField(validators=validate_with)

    return TimeInputForm
