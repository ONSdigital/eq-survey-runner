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
            self._update_answer(answer)
        else:
            self.answers.append(answer)

    def _update_answer(self, answer):
        for existing in self.find_existing(answer):
            existing['value'] = answer['value']
            break

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
                first['answer'] == second['answer'] and
                first['answer_instance'] == second['answer_instance'])

    def find_by_question(self, question_id):
        result = []
        for existing in self.answers:
            if existing['question'] == question_id:
                result.append(existing)

        return result
