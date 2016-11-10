class AnswerStore(object):
    """
    An object that stores the flattened structure of AnswerStates.
    It is referenced by the answers property in the QuestionnaireStore.
    """

    def __init__(self, existing_answers=[]):
        super(AnswerStore, self).__init__()
        self.answers = existing_answers

    def add(self, answer):
        """
        Add a new answer into the answer store.

        :param answer: A dict of flattened answer details.
        :return: None.
        """
        if self.exists(answer):
            self.update(answer)
        else:
            self.answers.append(answer)

    def update(self, answer):
        """
        Update the value of an answer already in the answer store.

        :param answer: A dict of flattened answer details.
        :return:
        """
        for index, existing in enumerate(self.answers):
            if self.same(existing, answer):
                self.answers[index]['value'] = answer['value']
                break

    def find(self, answer):
        """
        Finds all instances of an answer.

        :param answer: A dict of flattened answer details.
        :return:
        """
        found = []
        for existing in self.answers:
            if self.same(answer, existing):
                found.append(existing)

        return found

    def exists(self, answer):
        """
        Checks to see if an answer exists in the answer store.

        :param answer: A dict of flattened answer details.
        :return: True if the answer is in the store, False if not.
        """
        return self.count(answer) > 0

    def count(self, answer):
        """
        Count of the number of instances of an answer in the answer store.

        :param answer: A dict of flattened answer details.
        :return: 0 if the answer doesn't exist, otherwise the number of instances.
        """
        return len(self.find(answer))

    @classmethod
    def same(cls, first, second):
        """
        Check to see if two answers are the same.
        Two answers are considered the same if they share the same block, question, answer and instance Id.

        :param first: A dict of flattened answer details
        :param second: A dict of flattened answer details.
        :return: True if both answers are the same, otherwise False.
        """
        return (first['block_id'] == second['block_id'] and
                first['question_id'] == second['question_id'] and
                first['answer_id'] == second['answer_id'] and
                first['answer_instance'] == second['answer_instance'])

    def filter(self, filter_vars):
        filtered = []
        for answer in self.answers:
            matches = True
            for k, v in filter_vars.items():
                matches = matches and answer[k] == v
            if matches:
                filtered.append(answer)
        return filtered

    def find_by_question(self, question_id):
        """
        Helper method to find all answers in the answer store for a given question Id.

        :param question_id: The question Id.
        :return: A list of answer instances if the question has answers, otherwise an empty list.
        """
        result = []
        for existing in self.answers:
            if existing['question_id'] == question_id:
                result.append(existing)

        return result

    def find_by_block(self, block_id):
        result = []
        for existing in self.answers:
            if existing['block_id'] == block_id:
                result.append(existing)

        return result

    @staticmethod
    def as_key_value_pairs(answers):
        result = {}
        for answer in answers:
            answer_id = answer['answer_id']
            answer_id += str(answer['answer_instance']) if answer['answer_instance'] > 0 else ''
            result[answer_id] = answer['value']
        return result
