from flask import url_for


class Location(object):

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
        return hash(self.__dict__.values())

    def __str__(self):
        """
        String representation of the location, handy for debug messages

        :return:
        """
        return "{}/{}/{}".format(self.group_id, self.group_instance, self.block_id)

    def is_interstitial(self):
        return self.block_id in ['introduction', 'summary', 'thank-you']

    def url(self, metadata):
        """
        Return the survey runner url that this location represents

        :param metadata:
        :return:
        """
        collection_id = metadata["collection_exercise_sid"]
        form_type = metadata["form_type"]

        if self.is_interstitial():
            if self.block_id == 'summary':
                return url_for('questionnaire.get_summary',
                               form_type=form_type,
                               collection_id=collection_id)
            elif self.block_id == 'introduction':
                return url_for('questionnaire.get_introduction',
                               form_type=form_type,
                               collection_id=collection_id)
            elif self.block_id == 'confirmation':
                return url_for('questionnaire.get_confirmation',
                               form_type=form_type,
                               collection_id=collection_id)
            elif self.block_id == 'thank-you':
                return url_for('questionnaire.get_thank_you',
                               form_type=form_type,
                               collection_id=collection_id)
        return url_for('questionnaire.get_block',
                       form_type=form_type,
                       collection_id=collection_id,
                       group_id=self.group_id,
                       group_instance=self.group_instance,
                       block_id=self.block_id)
