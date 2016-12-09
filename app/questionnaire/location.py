from app.globals import get_metadata

from flask import url_for

from flask_login import current_user


class Location(object):
    def __init__(self, group_id, group_instance, block_id):

        self.group_id = group_id
        self.group_instance = group_instance
        self.block_id = block_id

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(self.__dict__.values())

    def __str__(self):
        return "{}/{}/{}".format(self.group_id, self.group_instance, self.block_id)

    def is_interstitial(self):
        return self.block_id in ['introduction', 'summary', 'thank-you']

    def url(self):
        metadata = get_metadata(current_user)

        eq_id = metadata["eq_id"]
        collection_id = metadata["collection_exercise_sid"]
        form_type = metadata["form_type"]

        if self.is_interstitial():
            if self.block_id == 'summary':
                return url_for('questionnaire.get_summary',
                               eq_id=eq_id,
                               form_type=form_type,
                               collection_id=collection_id)
            elif self.block_id == 'introduction':
                return url_for('questionnaire.get_introduction',
                               eq_id=eq_id,
                               form_type=form_type,
                               collection_id=collection_id)
            elif self.block_id == 'confirmation':
                return url_for('questionnaire.get_confirmation',
                               eq_id=eq_id,
                               form_type=form_type,
                               collection_id=collection_id)
            elif self.block_id == 'thank-you':
                return url_for('questionnaire.get_thank_you',
                               eq_id=eq_id,
                               form_type=form_type,
                               collection_id=collection_id)
        return url_for('questionnaire.get_block',
                       eq_id=eq_id,
                       form_type=form_type,
                       collection_id=collection_id,
                       group_id=self.group_id,
                       group_instance=self.group_instance,
                       block_id=self.block_id)
