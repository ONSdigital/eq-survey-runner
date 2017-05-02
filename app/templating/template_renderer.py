# coding: utf-8

import json

import re
from jinja2 import Environment

from app.jinja_filters import format_date, format_currency, format_household_member_name, format_household_summary


class TemplateRenderer:
    def __init__(self):
        self.environment = Environment()
        self.environment.filters['format_date'] = format_date
        self.environment.filters['format_currency'] = format_currency
        self.environment.filters['format_household_name'] = format_household_member_name
        self.environment.filters['format_household_summary'] = format_household_summary

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
