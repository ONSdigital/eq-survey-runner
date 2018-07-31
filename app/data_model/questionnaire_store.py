import simplejson as json

from app.data_model.answer_store import AnswerStore
from app.questionnaire.location import Location


class QuestionnaireStore:

    LATEST_VERSION = 1

    def __init__(self, storage, version=LATEST_VERSION):
        self._storage = storage
        self.version = version
        self.metadata = {}
        self.answer_store = AnswerStore()
        self.completed_blocks = []

        raw_data, version = self._storage.get_user_data()
        if raw_data:
            self._deserialise(raw_data)
        if version is not None:
            self.version = version

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

    def remove_completed_blocks(self, **kwargs):
        """removes completed blocks from store either by specific location
           or all group instances within a group and block"""

        if 'location' in kwargs:
            if kwargs['location'] in self.completed_blocks:
                self.completed_blocks.remove(kwargs['location'])
        else:
            self.completed_blocks = [completed_block for completed_block in self.completed_blocks
                                     if completed_block.group_id != kwargs['group_id'] or
                                     completed_block.block_id != kwargs['block_id']]

    def _encode_questionnaire_store(self, o):
        if hasattr(o, 'to_dict'):
            return o.to_dict()

        return json.JSONEncoder.default(self, o)
