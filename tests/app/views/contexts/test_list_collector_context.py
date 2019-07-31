from app.views.contexts.list_collector import _generate_list_item_title
from app.data_model.answer_store import AnswerStore, Answer

block_schema = {
    'id': 'add-person',
    'type': 'Question',
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
}


def test_generate_list_item_title_all_names():
    answer_store = AnswerStore()
    answer_store.add_or_update(Answer('first-name', ' John'))
    answer_store.add_or_update(Answer('last-name', '   Smith '))

    title = _generate_list_item_title(answer_store, block_schema)

    assert title == 'John Smith'


def test_generate_list_item_title_one_name():
    answer_store = AnswerStore()
    answer_store.add_or_update(Answer('first-name', ' John'))

    title = _generate_list_item_title(answer_store, block_schema)

    assert title == 'John'
