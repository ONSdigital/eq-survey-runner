import logging

from app.schema.widgets.date_widget import DateWidget

from flask import render_template

logger = logging.getLogger(__name__)


class MonthYearDateWidget(DateWidget):

    def render(self, answer_state):

        if answer_state.input:
            parts = answer_state.input.split('/')
        else:
            parts = [None, '']

        widget_params = {}
        widget_params['legend'] = answer_state.schema_item.label
        widget_params['fields'] = self._get_date_fields(parts)

        return render_template('partials/widgets/date_widget.html', **widget_params)

    def _get_date_fields(self, parts):

        fields = {}
        fields['month'] = self._get_month_field(parts[0])
        fields['year'] = self._get_year_field(parts[1])
        return fields

    def get_user_input(self, post_vars):

        if isinstance(post_vars, dict):
            if post_vars.get(self.name):
                try:
                    return post_vars.get(self.name).strftime('%m/%Y')
                except AttributeError:
                    return post_vars.get(self.name)
            else:
                month = post_vars.get(self.name + '-month', '')
                year = post_vars.get(self.name + '-year', '')

                return "{}/{}".format(month, year)

        else:
            return post_vars
