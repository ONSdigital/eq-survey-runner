# coding: utf-8

import re

import simplejson as json
from jinja2 import Environment

import app.jinja_filters as filters


class TemplateRenderer:
    def __init__(self):
        env = Environment(autoescape=True)

        env.filters['concatenated_list'] = filters.concatenated_list
        env.filters['format_date'] = filters.format_date
        env.filters['format_date_custom'] = filters.format_date_custom
        env.filters['format_household_name'] = filters.format_household_name
        env.filters['format_household_name_possessive'] = filters.format_household_name_possessive
        env.filters['format_household_summary'] = filters.format_household_summary
        env.filters['format_number'] = filters.format_number
        env.filters['format_repeating_summary'] = filters.format_repeating_summary
        env.filters['format_unordered_list'] = filters.format_unordered_list
        env.filters['get_currency_symbol'] = filters.get_currency_symbol

        env.globals['calculate_offset_from_weekday_in_last_whole_week'] = filters.calculate_offset_from_weekday_in_last_whole_week
        env.globals['calculate_years_difference'] = filters.calculate_years_difference
        env.globals['first_non_empty_item'] = filters.first_non_empty_item
        env.globals['format_address_list'] = filters.format_address_list
        env.globals['format_conditional_date'] = filters.format_conditional_date
        env.globals['format_currency'] = filters.format_currency
        env.globals['format_unit'] = filters.format_unit
        env.globals['format_date_range'] = filters.format_date_range
        env.globals['format_date_range_no_repeated_month_year'] = filters.format_date_range_no_repeated_month_year
        env.globals['format_unordered_list_missing_items'] = filters.format_unordered_list_missing_items
        env.globals['get_current_date'] = filters.get_current_date
        env.globals['max_value'] = filters.max_value
        env.globals['min_value'] = filters.min_value

        self.environment = env

    def render(self, renderable, **context):
        """Render.

        Substitute variables into renderable with the variables in context.

        :param (dict) renderable: Map of variables to be substituted.
        :param (dict) context: Map of variables to substitute.
        :returns (dict): The rendered version of the original renderable dict.
        """
        json_string = json.dumps(renderable) if isinstance(
            renderable, dict) else renderable
        template = self.environment.from_string(json_string)
        rendered = template.render(**context)
        result = rendered if isinstance(
            renderable, dict) else json.dumps(rendered)
        return json.loads(result)

    @staticmethod
    def safe_content(content):
        """Make content safe.

        Replaces variable with ellipsis and strips any HTML tags.

        :param (str) content: Input string.
        :returns (str): Modified string.
        """
        if content is not None:
            # Replace piping with ellipsis
            content = re.sub(r'{{.*?}}', '…', content)
            # Strip HTML Tags
            content = re.sub(r'</?[^>]+>', '', content)
        return content


renderer = TemplateRenderer()
