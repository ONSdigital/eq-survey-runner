from app.templating.summary.item import Item


class DateRangeSummaryItem(Item):
    def __init__(self, schema, state):
        super().__init__(schema, state)
        self.answer = "{}: {} {}: {}".format(schema.answers[0].label,
                                             state.answers[0].value.strftime(Item.DATE_FORMAT),
                                             schema.answers[1].label,
                                             state.answers[1].value.strftime(Item.DATE_FORMAT))
