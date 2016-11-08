class AnswerStore(object):
    """
    An object that stores the flattened structure of AnswerStates.
    It is referenced by the answers property in the QuestionnaireStore.
    """

    def __init__(self, existing_answers=[]):
        super(AnswerStore, self).__init__()
        self.answers = existing_answers

    def add_answer(self, answer):
        if self.exists(answer):
            self._insert_or_update(answer)
        else:
            self.answers.append(answer)

    def _insert_or_update(self, answer):
        is_new_instance = True
        for existing in self.find_existing(answer):
            if AnswerStore._same_instance(answer, existing):
                existing['value'] = answer['value']
                is_new_instance = False
                break

        if is_new_instance:
            self.answers.append(answer)

    def find_existing(self, answer):
        found = []
        for existing in self.answers:
            if AnswerStore._same_answer(answer, existing):
                found.append(answer)

        return found

    def exists(self, answer):
        return self.count(answer) > 0

    def count(self, answer):
        return len(self.find_existing(answer))

    @staticmethod
    def _same_answer(first, second):
        return (first['block'] == second['block'] and
                first['question'] == second['question'] and
                first['answer'] == second['answer'])

    @staticmethod
    def _same_instance(first, second):
        return first['answer_instance'] == second['answer_instance']
