from app.validation.validators import FormResponseRequired, TimeInputCheck
from wtforms import Form
from wtforms import StringField


def get_time_input_form(answer, error_messages):

    class TimeInputForm(Form):
        hours = StringField()
        mins = StringField()

    validate_with = []

    if not error_messages:
        time_input_messages = {}
    else:
        time_input_messages = error_messages.copy()

    if answer['mandatory'] is True:
        if 'validation' in answer and 'messages' in answer['validation'] \
                and 'MANDATORY' in answer['validation']['messages']:
            time_input_messages['MANDATORY'] = answer['validation']['messages']['MANDATORY']

        validate_with += [FormResponseRequired(message=time_input_messages['MANDATORY'])]

    if 'validation' in answer and 'messages' in answer['validation'] \
            and 'INVALID_TIME_INPUT' in answer['validation']['messages']:
        time_input_messages['INVALID_TIME'] = answer['validation']['messages']['INVALID_TIME_INPUT']

    validate_with += [TimeInputCheck(message=time_input_messages)]

    TimeInputForm.hours = StringField(validators=validate_with)

    return TimeInputForm
