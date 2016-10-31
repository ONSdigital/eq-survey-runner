from app.templating.summary.formatters.check_box import CheckBoxFormatter
from app.templating.summary.formatters.currency import CurrencyFormatter
from app.templating.summary.formatters.date_range import DateRangeFormatter
from app.templating.summary.formatters.radio_button import RadioButtonFormatter
from app.templating.summary.formatters.person_name import PersonNameFormatter


KNOWN_FORMATTERS = {
    "GENERAL": {
                'CHECKBOX': CheckBoxFormatter,
                'CURRENCY': CurrencyFormatter,
                'RADIO': RadioButtonFormatter,
    },
    "DATERANGE": {
                'DATE': DateRangeFormatter,
    },
    "HOUSEHOLD": {
                'COMPOSITE': PersonNameFormatter,
    },
}


class FormatterRegistry(object):

    @staticmethod
    def get_formatter(question_type, answer_type):

        if question_type in KNOWN_FORMATTERS:
            answer_formatters = KNOWN_FORMATTERS[question_type]
            answer_type = answer_type.upper()
            if answer_type in answer_formatters:
                return answer_formatters[answer_type]
