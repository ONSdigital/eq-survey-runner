from app.templating.summary.item import Item


class GeneralSummaryItem(Item):
    def __init__(self, schema, state):
        super().__init__(schema, state)
        self.answer = self.prepare_answer()

    def prepare_answer(self):
        if len(self.schema.answers) > 1:
            # Currently, the only multi-answer questions (apart from date ranges) are in the census test
            return None
        else:
            answer_type = self.schema.answers[0].type.upper()
            if self.state.answers[0].value:
                if answer_type == 'CURRENCY':
                    return self._prepare_currency_answer(self.state.answers[0].value)
                elif answer_type == 'DATE':
                    return self._prepare_date_value(self.state.answers[0].value)
                elif answer_type == 'RADIO':
                    return self._prepare_radio_value(self.state.answers[0].value)
                elif answer_type == 'CHECKBOX':
                    return self._prepare_checkbox_values(self.state.answers[0].value)
                else:
                    return self.state.answers[0].value
            else:
                return Item.MISSING_VALUE

    def _prepare_currency_answer(self, value):
        return Item.CURRENCY_SYMBOL + str(value)

    def _prepare_date_value(self, value):
        return value.strftime(Item.DATE_FORMAT)

    def _prepare_radio_value(self, value):
        for option in self.schema.answers[0].options:
            if option['value'] == value:
                return option['label']
        return Item.MISSING_VALUE

    def _prepare_checkbox_values(self, values):
        labels = []
        for option in self.schema.answers[0].options:
            if option['value'] in values:
                labels.append(option['label'])

        if len(labels) == 0:
            return Item.MISSING_VALUE
        else:
            return '<ul><li>' + '</li><li>'.join(labels) + '</li></ul>'
