class Answer:

    def __init__(self, block_id, answer_schema, answer):
        self.id = answer_schema['id']
        self.label = answer_schema['label']
        self.value = answer
        self.type = answer_schema['type'].lower()
        self.link = block_id + '#' + answer_schema['id']
