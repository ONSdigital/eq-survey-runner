class Answer:

    def __init__(self, answer_schema, answer):
        self.id = answer_schema['id']
        self.label = answer_schema.get('label')
        self.value = answer
        self.type = answer_schema['type'].lower()
        self.unit = answer_schema.get('unit')
        self.unit_length = answer_schema.get('unit_length')
        self.currency = answer_schema.get('currency')

    def serialize(self):
        return {
            'id': self.id,
            'label': self.label,
            'value': self.value,
            'type': self.type,
            'unit': self.unit,
            'unit_length': self.unit_length,
            'currency': self.currency,
        }
