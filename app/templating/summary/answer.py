class Answer:

    def __init__(self, answer_schema, answer, child_answer_value=None):
        self.id = answer_schema['id']
        self.label = answer_schema.get('label')
        self.value = answer
        self.type = answer_schema['type'].lower()
        self.parent_answer_id = answer_schema.get('parent_answer_id')
        self.child_answer_value = child_answer_value
