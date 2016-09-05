from app.templating.summary.summary_item import SummaryItem


class DateRangeSummaryItem(SummaryItem):
    def __init__(self, schema, state):
        super().__init__(schema, state)
        self.answer = [{
          'label': schema.answers[0].label,
          'value': state.answers[0].value,
        }, {
          'label': schema.answers[1].label,
          'value': state.answers[1].value,
        }]
