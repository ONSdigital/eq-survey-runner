class Answer:

    def __init__(self, answer_schema, answer, child_answer_value=None):
        self.id = answer_schema['id']
        self.label = answer_schema.get('label')
        self.value = answer
        self.type = answer_schema['type'].lower()
        self.unit = answer_schema.get('unit')
        self.parent_answer_id = answer_schema.get('parent_answer_id')
        self.child_answer_value = child_answer_value
        self.currency = answer_schema.get('currency')

    def serialize(self):
        return {
            'id': self.id,
            'label': self.label,
            'value': self.value,
            'type': self.type,
            'unit': self.unit,
            'parent_answer_id': self.parent_answer_id,
            'child_answer_value': self.child_answer_value,
            'currency': self.currency,
        }
