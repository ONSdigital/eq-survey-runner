class Answer:

    def __init__(self, answer_schema, answer):
        self.id = answer_schema['id']
        self.label = answer_schema['label'] if 'label' in answer_schema else None
        self.value = answer
        self.type = answer_schema['type'].lower()
