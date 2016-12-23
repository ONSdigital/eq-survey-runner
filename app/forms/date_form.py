import logging
import calendar

from wtforms import Form, FormField, SelectField, StringField
from wtforms import validators

from app.validation.validators import DateCheck, DateRangeCheck, DateRequired, MonthYearCheck

logger = logging.getLogger(__name__)


def get_date_form(answer=None, to_field_data=None, validate_range=False, error_messages={}):
    """
    Returns a date form metaclass with appropriate validators. Used in both date and
    date range form creation.

    :param error_messages: The messages during validation
    :param answer: The answer on which to base this form
    :param to_field_data: The data coming from the
    :param validate_range: Whether the dateform should add a daterange validator
    :return:
    """
    class DateForm(Form):

        MONTH_CHOICES = [('', 'Select month')] + [(str(x), calendar.month_name[x]) for x in range(1, 13)]

        month = SelectField(choices=MONTH_CHOICES, default='')
        year = StringField()

    validate_with = [validators.optional()]

    if answer['mandatory'] is True:
        if 'validation' in answer and 'messages' in answer['validation'] \
                and 'MANDATORY' in answer['validation']['messages']:
            error_messages['MANDATORY'] = answer['validation']['messages']['MANDATORY']

        validate_with = [DateRequired(message=error_messages['MANDATORY'])]

    if 'validation' in answer and 'messages' in answer['validation'] \
            and 'INVALID_DATE' in answer['validation']['messages']:
        error_messages['INVALID_DATE'] = answer['validation']['messages']['INVALID_DATE']

    validate_with += [DateCheck(error_messages['INVALID_DATE'])]

    if validate_range and to_field_data:
        validate_with += [DateRangeCheck(to_field_data=to_field_data, messages=error_messages)]

    DateForm.day = StringField(validators=validate_with)

    return DateForm


def get_month_year_form(answer, error_messages):

    class MonthYearDateForm(Form):
        year = StringField()

    month_choices = [('', 'Select month')] + [(str(x), calendar.month_name[x]) for x in range(1, 13)]

    validate_with = [validators.optional()]

    if answer['mandatory'] is True:
        error_message = error_messages['MANDATORY']
        if 'validation' in answer and 'messages' in answer['validation'] \
                and 'MANDATORY' in answer['validation']['messages']:
            error_message = answer['validation']['messages']['MANDATORY']

        validate_with = [DateRequired(message=error_message)]

    if 'validation' in answer and 'messages' in answer['validation'] \
            and 'INVALID_DATE' in answer['validation']['messages']:
        error_message = answer['validation']['messages']['INVALID_DATE']
        validate_with += [MonthYearCheck(error_message)]
    else:
        validate_with += [MonthYearCheck()]

    MonthYearDateForm.month = SelectField(choices=month_choices, default='', validators=validate_with)

    return MonthYearDateForm


def get_date_range_fields(question_json, to_field_data, error_messages):
    answer_from = question_json['answers'][0]
    answer_to = question_json['answers'][1]

    field_from = FormField(
        get_date_form(answer=answer_from, to_field_data=to_field_data, validate_range=True, error_messages=error_messages),
        label=answer_from['label'] if 'label' in answer_from else '',
        description=answer_from['guidance'] if 'guidance' in answer_from else '',
    )
    field_to = FormField(
        get_date_form(answer=answer_to, error_messages=error_messages),
        label=answer_to['label'] if 'label' in answer_to else '',
        description=answer_to['guidance'] if 'guidance' in answer_to else '',
    )

    return field_from, field_to


def get_date_data(form_data, answer_id):
    """
    Extract date from a form or serialised answer and return as a dict that wtforms would use

    :param form_data: The form data to search through
    :param answer_id: The answer_id to search for
    :return:
    """
    day_id = answer_id + '-day'
    month_id = answer_id + '-month'
    year_id = answer_id + '-year'

    if all(x in form_data for x in [day_id, month_id, year_id]):
        return {
            'day': form_data[day_id],
            'month': form_data[month_id],
            'year': form_data[year_id],
        }
    return None
