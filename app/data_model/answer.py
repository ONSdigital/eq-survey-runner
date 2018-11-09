from structlog import get_logger

logger = get_logger()


class Answer:
    def __init__(self, answer_id, value, group_instance_id=None, group_instance=0, answer_instance=0):
        if answer_id is None or value is None:
            raise ValueError("Both 'answer_id' and 'value' must be set for Answer")

        self.answer_id = answer_id
        self.group_instance_id = group_instance_id
        self.group_instance = group_instance
        self.answer_instance = answer_instance
        self.value = value

    def matches(self, answer):
        """
        Check to see if two answers match.
        Two answers are considered to match if they share the same answer_id, answer_instance and group_instance_id.

        :param answer: An answer to compare
        :return: True if both answers match, otherwise False.
        """
        return self.answer_id == answer.answer_id and \
            self.group_instance_id == answer.group_instance_id and \
            self.group_instance == answer.group_instance and \
            self.answer_instance == answer.answer_instance

    def matches_dict(self, answer_dict):
        """
        Check to see if a dict describes an answer the same as this object.

        :param answer_dict: A dictionary representation of the answer.
        :return: True if both answers match, otherwise False.
        """

        return self.matches(Answer(
            answer_dict.get('answer_id'),
            answer_dict.get('value'),
            answer_dict.get('group_instance_id'),
            answer_dict.get('group_instance', 0),
            answer_dict.get('answer_instance', 0),
        ))
