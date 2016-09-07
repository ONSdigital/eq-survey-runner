class SummaryItem(object):
    MISSING_VALUE = 'N/A'
    CURRENCY_SYMBOL = '£'
    DATE_FORMAT = '%d/%m/%Y'

    def __init__(self, schema, state):
        self.schema = schema
        self.state = state
        self.question = self.schema.title or self.schema.answers[0].label
        self.link = self.schema.container.container.id + '#' + self.schema.answers[0].id
        if len(self.schema.answers) > 0:
            self.type = self.schema.answers[0].type.lower()
