from app.data_model.answer_store import AnswerStore
from app.questionnaire.location import Location
import simplejson as json


class QuestionnaireStore:

    def __init__(self, storage):
        self._storage = storage
        self.metadata = {}
        self.answer_store = AnswerStore()
        self.completed_blocks = []

        raw_data = self._storage.get_user_data()
        if raw_data:
            self._deserialise(raw_data)

    def _deserialise(self, data):
        json_data = json.loads(data)
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
        self.answer_store.answers = []
        self.completed_blocks = []

    def add_or_update(self):
        data = self._serialise()
        self._storage.add_or_update(data=data)

    def _encode_questionnaire_store(self, o):
        if hasattr(o, 'to_dict'):
            return o.to_dict()

        return json.JSONEncoder.default(self, o)
