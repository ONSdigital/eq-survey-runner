# coding: utf-8

import json

import re
from jinja2 import Environment

from app.jinja_filters import format_date, format_household_member_name, format_currency, format_number,\
    get_currency_symbol, format_household_summary, format_str_as_date, format_conditional_date, format_list,\
    format_start_end_date, format_household_member_name_possessive


class TemplateRenderer:
    def __init__(self):
        self.environment = Environment()

        self.environment.filters['format_date'] = format_date
        self.environment.filters['format_str_as_date'] = format_str_as_date
        self.environment.filters['format_household_name'] = format_household_member_name
        self.environment.filters['format_household_name_possessive'] = format_household_member_name_possessive
        self.environment.filters['format_household_summary'] = format_household_summary
        self.environment.filters['format_list'] = format_list
        self.environment.globals['format_conditional_date'] = format_conditional_date
        self.environment.filters['format_currency'] = format_currency
        self.environment.filters['format_number'] = format_number
        self.environment.filters['get_currency_symbol'] = get_currency_symbol
        self.environment.globals['format_start_end_date'] = format_start_end_date

    def render(self, renderable, **context):
        """
        Substitute variables into renderable with the variables in context
        :param renderable: dict with variables to be substituted
        :param context: the variables to substitute
        :return: the rendered version of the original renderable dict
        """
        json_string = json.dumps(renderable) if isinstance(renderable, dict) else renderable
        template = self.environment.from_string(json_string)
        rendered = template.render(**context)
        result = rendered if isinstance(renderable, dict) else json.dumps(rendered)

        return json.loads(result)

    @staticmethod
    def safe_content(content):
        if content is not None:
            # Replace piping with ellipsis
            content = re.sub(r'\{\{[^}]+\}\}', '…', content)
            # Strip HTML Tags
            content = re.sub(r'</?[^>]+>', '', content)

        return content


renderer = TemplateRenderer()
