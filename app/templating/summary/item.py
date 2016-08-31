from app.utilities.factory import Factory


class Item(object):
    MISSING_VALUE = 'N/A'
    CURRENCY_SYMBOL = '£'
    DATE_FORMAT = '%d/%m/%Y'

    def __init__(self, schema, state):
        self.schema = schema
        self.state = state
        self.question = self.schema.title or self.schema.answers[0].label
        self.link = self.schema.container.container.id + '#' + self.schema.answers[0].id

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
