from types import MappingProxyType
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
        self._metadata = {}
        # metadata is a read-only view over self._metadata
        self.metadata = MappingProxyType(self._metadata)
        self.collection_metadata = {}
        self.answer_store = AnswerStore()
        self.completed_blocks = []

        raw_data, version = self._storage.get_user_data()
        if raw_data:
            self._deserialise(raw_data)
        if version is not None:
            self.version = version

    def get_latest_version_number(self):
        return self.LATEST_VERSION

    def set_metadata(self, to_set):
        """
        Set metadata. This should only be used where absolutely necessary.
        Metadata should normally be read only.
        """
        self._metadata = to_set
        self.metadata = MappingProxyType(self._metadata)

        return self

    def _deserialise(self, data):
        json_data = json.loads(data, use_decimal=True)
        completed_blocks = [Location.from_dict(location_dict=completed_block) for completed_block in
                            json_data.get('COMPLETED_BLOCKS', [])]
        self.set_metadata(json_data.get('METADATA', {}))
        self.answer_store = AnswerStore(json_data.get('ANSWERS'))
        self.completed_blocks = completed_blocks
        self.collection_metadata = json_data.get('COLLECTION_METADATA', {})

    def _serialise(self):
        data = {
            'METADATA': self._metadata,
            'ANSWERS': list(self.answer_store),
            'COMPLETED_BLOCKS': self.completed_blocks,
            'COLLECTION_METADATA': self.collection_metadata,
        }
        return json.dumps(data, default=self._encode_questionnaire_store)

    def delete(self):
        self._storage.delete()
        self._metadata.clear()
        self.collection_metadata = {}
        self.answer_store.clear()
        self.completed_blocks = []

    def add_or_update(self):
        data = self._serialise()
        self._storage.add_or_update(data=data)

    def remove_completed_blocks(self, location):
        """Removes completed blocks from store
        """
        self.completed_blocks.remove(location)

    def _encode_questionnaire_store(self, o):
        if hasattr(o, 'to_dict'):
            return o.to_dict()

        return json.JSONEncoder.default(self, o)
