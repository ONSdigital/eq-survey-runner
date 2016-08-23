from app.templating.summary.item import Item


class DateRangeSummaryItem(Item):
    def __init__(self, schema, state):
        super().__init__(schema, state)
        self.template_name = 'partials/summary/items/date_range.html'

    def get_template_params(self):
        template_params = {
            "question": self.schema.title,
            "start_date": self.state.answers[0].value.strftime(Item.DATE_FORMAT),
            "end_date": self.state.answers[1].value.strftime(Item.DATE_FORMAT),
            "link_id": self.schema.container.container.id,
        }
        return template_params
