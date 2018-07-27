import simplejson as json

from app.data_model.answer_store import AnswerStore
from app.questionnaire.location import Location


class QuestionnaireStore:
    LATEST_VERSION = 1

    def __init__(self, storage, version=None):
        self._storage = storage
        if version is None:
            version = self.get_latest_version_number()
        self.version = version
        self.metadata = {}
        self.answer_store = AnswerStore()
        self.completed_blocks = []

        raw_data, version = self._storage.get_user_data()
        if raw_data:
            self._deserialise(raw_data)
        if version is not None:
            self.version = version

    def get_latest_version_number(self):
        return self.LATEST_VERSION

    def _deserialise(self, data):
        json_data = json.loads(data, use_decimal=True)
        # pylint: disable=maybe-no-member
        completed_blocks = [Location.from_dict(location_dict=completed_block) for completed_block in
                            json_data.get('COMPLETED_BLOCKS', [])]
        self.metadata = json_data.get('METADATA', {})
        self.answer_store.answers = json_data.get('ANSWERS', [])
        self.completed_blocks = completed_blocks

    def _serialise(self):
        data = {
            'METADATA': self.metadata,
            'ANSWERS': self.answer_store.answers,
            'COMPLETED_BLOCKS': self.completed_blocks,
        }
        return json.dumps(data, default=self._encode_questionnaire_store)

    def delete(self):
        self._storage.delete()
        self.metadata = {}
        self.answer_store.clear()
        self.completed_blocks = []

    def add_or_update(self):
        data = self._serialise()
        self._storage.add_or_update(data=data, version=self.version)

    def remove_completed_blocks(self, location=None, group_id=None, block_id=None):
        """Removes completed blocks from store either by specific location
           or all group instances within a group and block.

            e.g.
            ```
            # By location
            question_store.remove_completed_blocks(location=Location(...))

            # By group_id/block_id (i.e. for all group instances for that group/block)
            question_store.remove_completed_blocks(group_id='a-test-group', block_id='a-test-block')
            ```
        """

        if location:
            if not isinstance(location, Location):
                raise TypeError('location needs to be a Location instance')
            self.completed_blocks.remove(location)
        else:
            if None in (group_id, block_id):
                raise KeyError('Both group_id and block_id required')

            self.completed_blocks = [completed_block for completed_block in self.completed_blocks
                                     if completed_block.group_id != group_id or
                                     completed_block.block_id != block_id]

    def _encode_questionnaire_store(self, o):
        if hasattr(o, 'to_dict'):
            return o.to_dict()

        return json.JSONEncoder.default(self, o)
