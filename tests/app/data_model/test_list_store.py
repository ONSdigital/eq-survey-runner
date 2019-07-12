from unittest.mock import patch

import pytest

from app.data_model.list_store import ListStore, ListModel


def test_list_serialisation():
    new_list = ListStore()

    first_id = new_list.add_list_item('people')
    second_id = new_list.add_list_item('people', primary_person=True)
    additional_list_id = new_list.add_list_item('pets')

    serialised = new_list.serialise()

    assert serialised == [
        {'name': 'people', 'primary_person': second_id, 'items': [second_id, first_id]},
        {'name': 'pets', 'items': [additional_list_id]},
    ]


def test_deserialisation():
    new_list = ListStore()
    # pylint: disable=protected-access
    first_id = new_list._generate_identifier()
    second_id = new_list._generate_identifier()
    additional_id = new_list._generate_identifier()

    serialised = [
        {'name': 'people', 'primary_person': second_id, 'items': [first_id, second_id]},
        {'name': 'pets', 'items': [additional_id]},
    ]

    deserialised = ListStore.deserialise(serialised)

    assert deserialised['people'].items == [first_id, second_id]
    assert deserialised['people'].primary_person == second_id
    assert deserialised['pets'].items == [additional_id]


def test_unique_id_generation():
    """
    Ensure that every id generated is unique per questionnaire.
    """
    # Mock the app.data_model.list_store.random_string method to return duplicates.
    with patch(
        'app.data_model.list_store.random_string',
        side_effect=['first', 'first', 'second'],
    ):
        list_store = ListStore()
        # pylint: disable=protected-access
        list_store._lists['test'] = ListModel(name='test', items=['first'])
        result = list_store._generate_identifier()

    assert result == 'second'


def test_get_item():
    store = ListStore()
    assert store['not_a_list'] == ListModel('not_a_list')


def test_delete_list_item_id():
    store = ListStore()
    person = store.add_list_item('people')
    store.delete_list_item('people', person)
    assert not store._lists  # pylint: disable=protected-access


def test_delete_list_item_id_does_not_raise():
    store = ListStore()
    store.add_list_item('people')
    try:
        store.delete_list_item('people', '123456')
    except ValueError:
        # Not necessary, but keeps it explicit.
        pytest.fail('Deleting a non-existant list item raised an error')


def test_list_representation_equal():
    assert ListModel(['123', '123']) != '123'

    assert ListModel(['1', '2']) == ListModel(['1', '2'])


def test_repr():
    test_list = ListModel('people', ['primaryperson'], primary_person='primaryperson')
    serialised = [
        {
            'name': 'people',
            'primary_person': 'primaryperson',
            'items': ['123', 'primaryperson'],
        }
    ]

    list_store = ListStore.deserialise(serialised)

    assert 'primary_person=primaryperson' in repr(test_list)
    assert "items=['primaryperson']" in repr(test_list)
    assert 'primaryperson' in repr(list_store)
