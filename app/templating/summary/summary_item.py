from app.utilities.factory import Factory


class SummaryItem(object):
    def __init__(self, schema, state):
        self.schema = schema
        self.state = state
        self.question = self.schema.title or self.schema.answers[0].label
        self.link = self.schema.container.container.id + '#' + self.schema.id
        if len(self.schema.answers) > 0:
            self.type = self.schema.answers[0].type.lower()

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
