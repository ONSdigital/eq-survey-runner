import pytest
from mock import MagicMock, Mock

from app.data_model.answer import Answer
from app.data_model.answer_store import AnswerStore
from app.data_model.list_store import ListStore
from app.forms.questionnaire_form import QuestionnaireForm
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.setup import create_app
from app.views.contexts import list_collector


@pytest.fixture
def rendered_block():
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
                        'parent_id': 'add-question',
                    },
                    {
                        'id': 'last-name',
                        'label': 'Last name',
                        'mandatory': True,
                        'type': 'TextField',
                        'parent_id': 'add-question',
                    },
                ],
                'parent_id': 'add-person',
            },
            'parent_id': 'list-collector',
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
                        'parent_id': 'edit-question',
                    },
                    {
                        'id': 'last-name',
                        'label': 'Last name',
                        'mandatory': True,
                        'type': 'TextField',
                        'parent_id': 'edit-question',
                    },
                ],
                'parent_id': 'edit-person',
            },
            'parent_id': 'list-collector',
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
                        'parent_id': 'remove-question',
                    }
                ],
                'parent_id': 'remove-person',
            },
            'parent_id': 'list-collector',
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
        'parent_id': 'group',
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
                    'parent_id': 'confirmation-question',
                }
            ],
            'parent_id': 'list-collector',
        },
    }


@pytest.fixture
def answer_store():
    return AnswerStore(
        [
            {'answer_id': 'first-name', 'value': 'Toni', 'list_item_id': 'PlwgoG'},
            {'answer_id': 'last-name', 'value': 'Morrison', 'list_item_id': 'PlwgoG'},
            {'answer_id': 'first-name', 'value': 'Barry', 'list_item_id': 'UHPLbX'},
            {'answer_id': 'last-name', 'value': 'Pheloung', 'list_item_id': 'UHPLbX'},
        ]
    )


@pytest.fixture
def list_store():
    return ListStore([{'items': ['PlwgoG', 'UHPLbX', 'FnoDHP'], 'name': 'people'}])


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
    return Mock(QuestionnaireSchema({}))


@pytest.fixture
def app():
    setting_overrides = {'LOGIN_DISABLED': True}
    app = create_app(setting_overrides=setting_overrides)
    app._app_context = app.app_context()

    return app


def test_build_list_collector_context(
    rendered_block, schema, answer_store, list_store, form, app
):
    context = list_collector.build_list_collector_context(
        rendered_block, schema, answer_store, list_store, 'en', form
    )

    assert all(
        keys in context.keys() for keys in ['block', 'form', 'list_items', 'add_link']
    )
    assert context['add_link'] == '/questionnaire/people/list-collector/'


def test_build_list_collector_context_no_summary(
    rendered_block, schema, answer_store, list_store, form, app
):
    del rendered_block['summary']
    context = list_collector.build_list_collector_context(
        rendered_block, schema, answer_store, list_store, 'en', form
    )

    assert context['list_items'] == []


def test_build_list_items_summary_context(
    rendered_block, schema, answer_store, list_store, app
):
    expected = [
        {
            'answers': [
                Answer(answer_id='first-name', value='Toni', list_item_id='PlwgoG'),
                Answer(answer_id='last-name', value='Morrison', list_item_id='PlwgoG'),
            ],
            'item_title': 'Toni Morrison',
            'edit_link': '/questionnaire/people/PlwgoG/edit-person/',
            'remove_link': '/questionnaire/people/PlwgoG/remove-person/',
            'primary_person': False,
        },
        {
            'answers': [
                Answer(answer_id='first-name', value='Barry', list_item_id='UHPLbX'),
                Answer(answer_id='last-name', value='Pheloung', list_item_id='UHPLbX'),
            ],
            'item_title': 'Barry Pheloung',
            'edit_link': '/questionnaire/people/UHPLbX/edit-person/',
            'remove_link': '/questionnaire/people/UHPLbX/remove-person/',
            'primary_person': False,
        },
        {
            'answers': [],
            'item_title': '',
            'edit_link': '/questionnaire/people/FnoDHP/edit-person/',
            'remove_link': '/questionnaire/people/FnoDHP/remove-person/',
            'primary_person': False,
        },
    ]

    actual = list_collector.build_list_items_summary_context(
        rendered_block, schema, answer_store, list_store, 'en'
    )

    assert expected == actual


def test_assert_primary_person_string_appended(
    rendered_block, schema, answer_store, list_store, app
):
    list_store['people'].primary_person = 'PlwgoG'
    list_item_context = list_collector.build_list_items_summary_context(
        rendered_block, schema, answer_store, list_store, 'en'
    )

    assert list_item_context[0]['primary_person'] == True
    assert 'Toni Morrison (You)' == list_item_context[0]['item_title']
    assert 'Barry Pheloung' == list_item_context[1]['item_title']
