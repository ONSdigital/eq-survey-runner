import pytest

from app.questionnaire.location import Location
from app.views.contexts.summary.group import Group


@pytest.fixture(name='schema')
def fixture_schema():
    return {
        'blocks': [
            {
                'type': 'Question',
                'id': 'number-question-one',
                'question': {
                    'answers': [
                        {
                            'id': 'answer-one',
                            'mandatory': False,
                            'type': 'Number',
                            'label': 'Leave blank',
                            'default': 0,
                        }
                    ],
                    'id': 'question',
                    'title': "Don't enter an answer. A default value will be used",
                    'type': 'General',
                },
            },
            {
                'type': 'Question',
                'id': 'number-question-two',
                'show_on_section_summary': False,
                'question': {
                    'answers': [
                        {
                            'id': 'answer-two',
                            'mandatory': False,
                            'type': 'Number',
                            'label': 'Enter a Value',
                        }
                    ],
                    'id': 'question2',
                    'title': 'Enter an answer. It will be shown on the summary page',
                    'type': 'General',
                },
            },
            {'type': 'Summary', 'id': 'summary'},
        ],
        'id': 'group',
        'title': 'group-test',
    }


@pytest.fixture(name='path')
def fixture_path():
    return [
        Location('section', 'number-question-one'),
        Location('section', 'number-question-two'),
    ]


def test_group_serialize_hide_on_summary_true(
    app, mocker, schema, path
):  # pylint: disable=unused-argument

    answer_store = mocker.MagicMock()
    list_store = mocker.MagicMock()
    metadata = mocker.MagicMock()

    group = Group(
        schema,
        path,
        answer_store,
        list_store,
        metadata,
        None,
        Location('test', 'test'),
        'en',
    )

    assert len(group.blocks) == 1
    assert group.blocks[0]['id'] == 'number-question-one'


def test_group_serialize_hide_on_summary_not_set(
    app, mocker, schema, path
):  # pylint: disable=unused-argument

    answer_store = mocker.MagicMock()
    list_store = mocker.MagicMock()
    metadata = mocker.MagicMock()

    del schema['blocks'][1]['show_on_section_summary']

    group = Group(
        schema,
        path,
        answer_store,
        list_store,
        metadata,
        None,
        Location('test', 'test'),
        'en',
    )

    assert len(group.blocks) == 2
    assert group.blocks[1]['id'] == 'number-question-two'


def test_group_serialize_hide_on_summary_false(
    app, mocker, schema, path
):  # pylint: disable=unused-argument
    answer_store = mocker.MagicMock()
    list_store = mocker.MagicMock()
    metadata = mocker.MagicMock()

    schema['blocks'][0]['show_on_section_summary'] = True
    schema['blocks'][1]['show_on_section_summary'] = True

    group = Group(
        schema,
        path,
        answer_store,
        list_store,
        metadata,
        None,
        Location('test', 'test'),
        'en',
    )

    assert len(group.blocks) == 2
    assert group.blocks[1]['id'] == 'number-question-two'
