from flask import url_for


class Location:

    def __init__(self, group_id, group_instance, block_id):

        self.group_id = group_id
        self.group_instance = group_instance
        self.block_id = block_id

    def __eq__(self, other):
        """
        Check to see if two locations are equal.
        Two answers are considered to be equal if their dictionary representations equal one another.

        :param other: An answer to compare
        :return: True if both answers match, otherwise False.
        """
        return isinstance(other, Location) and self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(frozenset(self.__dict__.values()))

    def __str__(self):
        """
        String representation of the location, handy for debug messages

        :return:
        """
        return '{}/{}/{}'.format(self.group_id, self.group_instance, self.block_id)

    def __repr__(self):
        """
        String representation of the location, handy for debug messages

        :return:
        """
        return str(self)

    @classmethod
    def from_dict(cls, location_dict):
        group_id = location_dict['group_id']
        group_instance = location_dict['group_instance']
        block_id = location_dict['block_id']
        return cls(group_id, group_instance, block_id)

    def to_dict(self):
        return vars(self)

    def url(self, metadata):
        """
        Return the survey runner url that this location represents

        :param metadata:
        :return:
        """
        eq_id = metadata['eq_id']
        collection_id = metadata['collection_exercise_sid']
        form_type = metadata['form_type']

        return url_for('questionnaire.get_block',
                       eq_id=eq_id,
                       form_type=form_type,
                       collection_id=collection_id,
                       group_id=self.group_id,
                       group_instance=self.group_instance,
                       block_id=self.block_id)
