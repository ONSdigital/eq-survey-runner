from app.data_model.answer import Answer
from app.utilities.schema import load_schema_from_name
from app.views.contexts import list_collector
from app.questionnaire.questionnaire_schema import DEFAULT_LANGUAGE_CODE


def test_build_list_collector_context(
    list_collector_block, schema, people_answer_store, people_list_store, form, app
):

    context = list_collector.build_list_collector_context(
        list_collector_block,
        schema,
        people_answer_store,
        people_list_store,
        DEFAULT_LANGUAGE_CODE,
        form,
    )

    assert all(
        keys in context.keys() for keys in ['block', 'form', 'list_items', 'add_link']
    )
    assert context['add_link'] == '/questionnaire/people/list-collector/'


def test_build_list_collector_context_no_summary(
    list_collector_block, schema, people_answer_store, people_list_store, form, app
):
    del list_collector_block['summary']
    context = list_collector.build_list_collector_context(
        list_collector_block,
        schema,
        people_answer_store,
        people_list_store,
        DEFAULT_LANGUAGE_CODE,
        form,
    )

    assert context['list_items'] == []


def test_build_list_items_summary_context(
    list_collector_block, people_answer_store, people_list_store, app
):

    schema = load_schema_from_name('test_list_collector_primary_person')
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
        list_collector_block,
        schema,
        people_answer_store,
        people_list_store,
        DEFAULT_LANGUAGE_CODE,
    )

    assert expected == actual


def test_assert_primary_person_string_appended(
    list_collector_block, people_answer_store, people_list_store, app
):
    schema = load_schema_from_name('test_list_collector_primary_person')
    people_list_store['people'].primary_person = 'PlwgoG'
    list_item_context = list_collector.build_list_items_summary_context(
        list_collector_block,
        schema,
        people_answer_store,
        people_list_store,
        DEFAULT_LANGUAGE_CODE,
    )

    assert list_item_context[0]['primary_person'] is True
    assert 'Toni Morrison (You)' == list_item_context[0]['item_title']
    assert 'Barry Pheloung' == list_item_context[1]['item_title']
