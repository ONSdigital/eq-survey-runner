from unittest.mock import patch
from app.data_model.list_store import ListStore

def test_list_serialisation():
    new_list = ListStore()

    first_id = new_list.add_list_item('people')
    second_id = new_list.add_list_item('people')
    additional_list_id = new_list.add_list_item('pets')

    serialised = new_list.serialise()

    assert serialised == [
        {
            'name': 'people',
            'items': [
                first_id,
                second_id
            ]
        },
        {
            'name': 'pets',
            'items': [
                additional_list_id
            ]
        }
    ]


def test_deserialisation():
    new_list = ListStore()
    #pylint: disable=protected-access
    first_id = new_list._generate_identifier()
    second_id = new_list._generate_identifier()
    additional_id = new_list._generate_identifier()

    serialised = [
        {
            'name': 'people',
            'items': [
                first_id,
                second_id
            ]
        },
        {
            'name': 'pets',
            'items': [
                additional_id
            ]
        }
    ]

    deserialised = ListStore.deserialise(serialised)

    assert deserialised['people'] == [first_id, second_id]
    assert deserialised['pets'] == [additional_id]

def test_unique_id_generation():
    """
    Ensure that every id generated is unique per questionnaire.
    """
    # Mock the app.data_model.list_store.random_string method to return duplicates.
    with patch('app.data_model.list_store.random_string', side_effect=['first', 'first', 'second']):
        list_store = ListStore()
        #pylint: disable=protected-access
        list_store._lists['test'] = ['first']
        result = list_store._generate_identifier()

    assert result == 'second'

def test_get_item():
    store = ListStore()

    assert store['not_an_list'] == []

def test_delete_list_item_id():
    store = ListStore()
    person = store.add_list_item('people')
    store.delete_list_item_id('people', person)
    assert not store._lists # pylint: disable=protected-access
