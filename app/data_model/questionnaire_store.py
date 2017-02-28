import json

from app.data_model.answer_store import AnswerStore
from app.questionnaire.location import Location


class QuestionnaireStore:

    def __init__(self, storage):
        self._storage = storage
        self._initial_data = {}
        self.metadata = {}
        self.answer_store = AnswerStore()
        self.completed_blocks = []

        raw_data = self._storage.get_user_data()
        if raw_data:
            self._initial_data = self._deserialise(raw_data)
            data_copy = self._deserialise(raw_data)
            self._set_data(data_copy)

    @staticmethod
    def _deserialise(raw_data):
        data = json.loads(raw_data)
        data['COMPLETED_BLOCKS'] = [Location.from_dict(location_dict=completed_block) for completed_block in data['COMPLETED_BLOCKS']]
        return data

    @staticmethod
    def _serialise(data):
        # Override default function to return object as a dict
        return json.dumps(data, default=lambda o: o.__dict__)

    def _set_data(self, data):
        self.metadata = data.get('METADATA') or {}
        self.answer_store.answers = data.get('ANSWERS') or []
        self.completed_blocks = data.get('COMPLETED_BLOCKS') or []

    def _get_data(self):
        return {
            'METADATA': self.metadata,
            'ANSWERS': self.answer_store.answers,
            'COMPLETED_BLOCKS': self.completed_blocks,
        }

    def has_changed(self):
        return self._initial_data != self._get_data()

    def delete(self):
        self._storage.delete()
        self._set_data(data={})
        self._initial_data = {}

    def add_or_update(self):
        data = self._get_data()
        serialised_data = self._serialise(data)
        self._storage.add_or_update(data=serialised_data)
