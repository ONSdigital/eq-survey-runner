import pytest
from mock import MagicMock

from app.data_model.answer_store import AnswerStore
from app.data_model.list_store import ListStore
from app.forms.questionnaire_form import QuestionnaireForm
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.setup import create_app


@pytest.fixture
def app():
    app = create_app(
        setting_overrides={'LOGIN_DISABLED': True, 'SERVER_NAME': 'test.localdomain'}
    )
    context = app.app_context()
    context.push()

    return app


@pytest.fixture
def list_collector_block():
    return {
        'id': 'list-collector',
        'type': 'ListCollector',
        'for_list': 'people',
        'add_answer': {'id': 'anyone-else', 'value': 'Yes'},
        'remove_answer': {'id': 'remove-confirmation', 'value': 'Yes'},
        'add_block': {
            'id': 'add-person',
            'type': 'ListAddQuestion',
            'question': {
                'id': 'add-question',
                'type': 'General',
                'title': 'What is the name of the person?',
                'answers': [
                    {
                        'id': 'first-name',
                        'label': 'First name',
                        'mandatory': True,
                        'type': 'TextField',
                    },
                    {
                        'id': 'last-name',
                        'label': 'Last name',
                        'mandatory': True,
                        'type': 'TextField',
                    },
                ],
            },
        },
        'edit_block': {
            'id': 'edit-person',
            'type': 'ListEditQuestion',
            'question': {
                'id': 'edit-question',
                'type': 'General',
                'title': 'What is the name of the person?',
                'answers': [
                    {
                        'id': 'first-name',
                        'label': 'First name',
                        'mandatory': True,
                        'type': 'TextField',
                    },
                    {
                        'id': 'last-name',
                        'label': 'Last name',
                        'mandatory': True,
                        'type': 'TextField',
                    },
                ],
            },
        },
        'remove_block': {
            'id': 'remove-person',
            'type': 'ListRemoveQuestion',
            'question': {
                'id': 'remove-question',
                'type': 'General',
                'title': 'Are you sure you want to remove this person?',
                'answers': [
                    {
                        'id': 'remove-confirmation',
                        'mandatory': True,
                        'type': 'Radio',
                        'options': [
                            {'label': 'Yes', 'value': 'Yes'},
                            {'label': 'No', 'value': 'No'},
                        ],
                    }
                ],
            },
        },
        'summary': {
            'item_title': {
                'text': '{person_name}',
                'placeholders': [
                    {
                        'placeholder': 'person_name',
                        'transforms': [
                            {
                                'arguments': {
                                    'delimiter': ' ',
                                    'list_to_concatenate': {
                                        'identifier': ['first-name', 'last-name'],
                                        'source': 'answers',
                                    },
                                },
                                'transform': 'concatenate_list',
                            }
                        ],
                    }
                ],
            }
        },
        'question': {
            'id': 'confirmation-question',
            'type': 'General',
            'title': 'Does anyone else live here?',
            'answers': [
                {
                    'id': 'anyone-else',
                    'mandatory': True,
                    'type': 'Radio',
                    'options': [
                        {'label': 'Yes', 'value': 'Yes'},
                        {'label': 'No', 'value': 'No'},
                    ],
                }
            ],
        },
    }


@pytest.fixture
def form():
    mock_form = MagicMock(
        spec=QuestionnaireForm,
        data={'first-name': 'Toni', 'last-name': 'Morrison'},
        errors={},
        question_errors={},
        fields={},
    )
    mock_form.answer_errors.return_value = ''
    return mock_form


@pytest.fixture
def schema():
    return MagicMock(QuestionnaireSchema({}))


@pytest.fixture
def people_answer_store():
    return AnswerStore(
        [
            {'answer_id': 'first-name', 'value': 'Toni', 'list_item_id': 'PlwgoG'},
            {'answer_id': 'last-name', 'value': 'Morrison', 'list_item_id': 'PlwgoG'},
            {'answer_id': 'first-name', 'value': 'Barry', 'list_item_id': 'UHPLbX'},
            {'answer_id': 'last-name', 'value': 'Pheloung', 'list_item_id': 'UHPLbX'},
        ]
    )


@pytest.fixture
def people_list_store():
    return ListStore([{'items': ['PlwgoG', 'UHPLbX', 'FnoDHP'], 'name': 'people'}])
