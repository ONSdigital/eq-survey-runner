# pylint: disable=redefined-outer-name
import uuid
from unittest.mock import MagicMock

import pytest

from app.data_model.answer_store import AnswerStore
from app.data_model.answer import Answer
from app.data_model.questionnaire_store import QuestionnaireStore
from app.storage.metadata_parser import (
    validate_questionnaire_claims,
    validate_runner_claims,
)
from app.questionnaire.questionnaire_schema import QuestionnaireSchema


@pytest.fixture
def fake_metadata():
    def parse_metadata(claims, schema_metadata):
        runner_claims = validate_runner_claims(claims)
        questionnaire_claims = validate_questionnaire_claims(claims, schema_metadata)
        return {**runner_claims, **questionnaire_claims}

    schema_metadata = [
        {'name': 'user_id', 'type': 'string'},
        {'name': 'period_id', 'type': 'string'},
        {'name': 'ref_p_start_date', 'type': 'string'},
        {'name': 'ref_p_end_date', 'type': 'string'},
        {'name': 'display_address', 'type': 'string'},
        {'name': 'case_ref', 'type': 'string'},
    ]

    metadata = parse_metadata(
        {
            'tx_id': str(uuid.uuid4()),
            'user_id': '789473423',
            'schema_name': '1_0000',
            'collection_exercise_sid': 'test-sid',
            'account_service_url': 'https://rh.ons.gov.uk/',
            'period_id': '2016-02-01',
            'period_str': '2016-01-01',
            'ref_p_start_date': '2016-02-02',
            'ref_p_end_date': '2016-03-03',
            'ru_ref': '432423423423',
            'response_id': '1234567890123456',
            'ru_name': 'Apple',
            'return_by': '2016-07-07',
            'case_id': str(uuid.uuid4()),
            'display_address': '68 Abingdon Road, Goathill',
            'questionnaire_id': '0123456789000000',
            'case_ref': '1000000000000001',
            'jti': str(uuid.uuid4()),
        },
        schema_metadata,
    )

    return metadata


@pytest.fixture
def fake_collection_metadata():
    collection_metadata = {'started_at': '2018-07-04T14:49:33.448608+00:00'}
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
    questionnaire = {'survey_id': '021', 'data_version': '0.0.3'}

    return QuestionnaireSchema(questionnaire)
