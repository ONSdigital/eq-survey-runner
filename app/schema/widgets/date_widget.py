import calendar
import logging

from app.libs.utils import ObjectFromDict
from app.schema.widget import Widget

from flask import render_template

logger = logging.getLogger(__name__)


class DateWidget(Widget):
    def render(self, answer_state):

        if answer_state.input:
            parts = answer_state.input.split('/')
        else:
            parts = ['', None, '']

        widget_params = {'legend': answer_state.schema_item.label,
                         'fields': self._get_date_fields(parts, answer_state.schema_item.mandatory)}

        return render_template('partials/widgets/date_widget.html', **widget_params)

    def _get_date_fields(self, parts, is_mandatory):

        return {'day': self._get_day_field(parts[0]),
                'month': self._get_month_field(parts[1], is_mandatory),
                'year': self._get_year_field(parts[2])}

    def _get_day_field(self, day):

        return {
            'label': {
                'for': self.name + '-day',
                'text': 'Day',
            },
            'input': {
                'type': 'text',
                'value': day,
                'placeholder': 'DD',
                'name': self.name + '-day',
                'id': self.id + '-day',
                'maxlength': '2',
            },
        }

    def _get_month_field(self, month, is_mandatory):

        return {

                'label': {
                    'for': self.name + '-month',
                    'text': 'Month',
                },
                'select': {
                    'placeholder': 'Select month',
                    'options': self._get_months(month, is_mandatory),
                    'name': self.name + '-month',
                    'id': self.name + '-month',
                  },
                }

    def _get_year_field(self, year):

        return {
            'label': {
                'for': self.name + '-year',
                'text': 'Year',
            },
            'input': {
                'value': year,
                'type': 'text',
                'placeholder': 'YYYY',
                'name': self.name + '-year',
                'id': self.name + '-year',
                'maxlength': '4',
            },
        }

    @staticmethod
    def _get_months(selected_month, is_mandatory):
        if selected_month:
            selected_month = int(selected_month)

        months = []

        months.append(ObjectFromDict({
            'value': '',
            'text': 'Select month',
            'disabled': True if is_mandatory else False,
            'selected': False if selected_month else True,
        }))

        for month in range(1, 13):
            months.append(ObjectFromDict({
                'value': month,
                'text': calendar.month_name[month],
                'selected': (selected_month == month),
                'disabled': False,
            }))
        return months

    def get_user_input(self, post_vars):
        # Todo, this needs a refactor, we currently have 3 types being passed in post_vars: datetime, string and dict
        if isinstance(post_vars, dict):
            if post_vars.get(self.name):
                try:
                    return post_vars.get(self.name).strftime('%d/%m/%Y')
                except AttributeError:
                    return post_vars.get(self.name)
            else:
                day = post_vars.get(self.name + '-day', '')
                month = post_vars.get(self.name + '-month', '')
                year = post_vars.get(self.name + '-year', '')

                if day or month or year:
                    return "{}/{}/{}".format(day, month, year)
                else:
                    return None

        else:
            return post_vars
