# pylint: disable=redefined-outer-name
import uuid
from unittest.mock import MagicMock

import pytest

from app.data_model.answer_store import AnswerStore
from app.data_model.answer import Answer
from app.data_model.questionnaire_store import QuestionnaireStore
from app.storage.metadata_parser import validate_metadata, parse_runner_claims
from app.questionnaire.questionnaire_schema import QuestionnaireSchema


@pytest.fixture
def fake_metadata():
    def parse_metadata(claims, schema_metadata):
        validated_claims = parse_runner_claims(claims)
        validate_metadata(validated_claims, schema_metadata)
        return validated_claims

    schema_metadata = [
        {
            'name': 'user_id',
            'validator': 'string'
        },
        {
            'name': 'period_id',
            'validator': 'string'
        }
    ]

    metadata = parse_metadata({
        'tx_id': str(uuid.uuid4()),
        'user_id': '789473423',
        'form_type': '0000',
        'collection_exercise_sid': 'test-sid',
        'eq_id': '1',
        'period_id': '2016-02-01',
        'period_str': '2016-01-01',
        'ref_p_start_date': '2016-02-02',
        'ref_p_end_date': '2016-03-03',
        'ru_ref': '432423423423',
        'ru_name': 'Apple',
        'return_by': '2016-07-07',
        'started_at': '2018-07-04T14:49:33.448608+00:00',
        'case_id': str(uuid.uuid4()),
        'case_ref': '1000000000000001'
    }, schema_metadata)

    return metadata


@pytest.fixture
def fake_collection_metadata():
    collection_metadata = {
        'started_at': '2018-07-04T14:49:33.448608+00:00',
    }

    return collection_metadata


@pytest.fixture
def fake_questionnaire_store(fake_metadata, fake_collection_metadata):
    user_answer = Answer(answer_id='GHI', value=0, list_item_id=None)

    storage = MagicMock()
    storage.get_user_data = MagicMock(return_value=('{}', 1))
    storage.add_or_update = MagicMock()

    store = QuestionnaireStore(storage)

    store.answer_store = AnswerStore()
    store.answer_store.add_or_update(user_answer)
    store.metadata = fake_metadata
    store.collection_metadata = fake_collection_metadata

    return store


@pytest.fixture
def fake_questionnaire_schema():
    questionnaire = {
        'survey_id': '021',
        'data_version': '0.0.3'
    }

    return QuestionnaireSchema(questionnaire)
