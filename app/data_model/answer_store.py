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
        for existing in self.find(answer):
            existing['value'] = answer['value']
            break

    def find(self, answer):
        """
        Finds all instances of an answer.

        :param answer: A dict of flattened answer details.
        :return:
        """
        found = []
        for existing in self.answers:
            if AnswerStore.same(answer, existing):
                found.append(answer)

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

    @staticmethod
    def same(first, second):
        """
        Check to see if two answers are the same.
        Two answers are considered the same if they share the same block, question, answer and instance Id.

        :param first: A dict of flattened answer details
        :param second: A dict of flattened answer details.
        :return: True if both answers are the same, otherwise False.
        """
        return (first['block'] == second['block'] and
                first['question'] == second['question'] and
                first['answer'] == second['answer'] and
                first['answer_instance'] == second['answer_instance'])

    def find_by_question(self, question_id):
        """
        Helper method to find all answers in the answer store for a given question Id.

        :param question_id: The question Id.
        :return: A list of answer instances if the question has answers, otherwise an empty list.
        """
        result = []
        for existing in self.answers:
            if existing['question'] == question_id:
                result.append(existing)

        return result

    def find_by_block(self, block_id):
        result = []
        for existing in self.answers:
            if existing['block'] == block_id:
                result.append(existing)

        return result

    @staticmethod
    def as_key_value_pairs(answers):
        result = {}
        for answer in answers:
            answer_id = answer['answer'] + str(answer['answer_instance']) if answer['answer_instance'] > 0 else ''
            result[answer_id] = answer['value']
        return result
