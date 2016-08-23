from app.utilities.factory import Factory

from flask import render_template


class Item(object):
    MISSING_VALUE = 'N/A'
    CURRENCY_SYMBOL = '£'
    DATE_FORMAT = '%d/%m/%Y'

    def __init__(self, schema, state):
        self.schema = schema
        self.state = state

    @staticmethod
    def create_item(schema, state):
        from app.templating.summary.items.date_range_summary import DateRangeSummaryItem
        from app.templating.summary.items.general_summary import GeneralSummaryItem

        factory = Factory()
        factory.register_all({
            "DATERANGE": DateRangeSummaryItem,
            "GENERAL": GeneralSummaryItem,
        })
        return factory.create(schema.type.upper(), schema, state)

    def get_template_params(self):
        return {}

    def render(self):
        template_params = self.get_template_params()
        return render_template(self.template_name, **template_params)
