import calendar
import logging

from app.libs.utils import ObjectFromDict
from app.schema.widget import Widget

from flask import render_template

logger = logging.getLogger(__name__)


class DateWidget(Widget):
    def _get_days(self, selected_day):
        if selected_day:
            selected_day = int(selected_day)

        days = []
        for day in range(1, 32):
            days.append(ObjectFromDict({
                'value': day,
                'text': day,
                'selected': (selected_day == day),
                'disabled': False,
            }))
        return days

    def _get_months(self, selected_month):
        if selected_month:
            selected_month = int(selected_month)

        months = []
        for month in range(1, 13):
            months.append(ObjectFromDict({
                'value': month,
                'text': calendar.month_name[month],
                'selected': (selected_month == month),
                'disabled': False,
            }))
        return months

    def render(self, answer_state):
        if answer_state.input:
            parts = answer_state.input.split('/')
        else:
            parts = [None, None, '']

        widget_params = {
            'legend': answer_state.schema_item.label,
            'fields': {
                'day': {
                  'label': {
                    'for': self.name + '-day',
                    'text': 'Day',
                  },
                  'input': {
                    'value': parts[0],
                    'placeholder': 'DD',
                    'name': self.name + '-day',
                    'id': self.name + '-day',
                  },
                },
                'month': {
                  'label': {
                    'for': self.name + '-month',
                    'text': 'Month',
                  },
                  'select': {
                    'options': self._get_months(parts[1]),
                    'name': self.name + '-month',
                    'id': self.name + '-month',
                  },
                },
                'year': {
                  'label': {
                    'for': self.name + '-year',
                    'text': 'Year',
                  },
                  'input': {
                    'value': parts[2],
                    'placeholder': 'YYYY',
                    'name': self.name + '-year',
                    'id': self.name + '-year',
                  },
                },
            },
        }

        return render_template('partials/widgets/date_widget.html', **widget_params)

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

                # if day or month or year:
                return "{}/{}/{}".format(day, month, year)

        else:
            return post_vars
