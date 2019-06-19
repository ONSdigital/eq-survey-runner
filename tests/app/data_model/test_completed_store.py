from app.data_model.completed_store import CompletedStore
from app.questionnaire.location import Location


def test_serialisation():
    store = CompletedStore()

    store.add_completed_location(Location('one'))
    store.add_completed_location(Location('two'))
    store.add_completed_section('s1')

    serialised = store.serialise()

    assert serialised == {
        'locations': [{'block_id': 'one'}, {'block_id': 'two'}],
        'sections': ['s1'],
    }


def test_deserialisation():
    completed = {
        'locations': [{'block_id': 'one'}, {'block_id': 'two'}],
        'sections': ['s1'],
    }
    store = CompletedStore(completed)

    assert store.locations == [Location(block_id='one'), Location(block_id='two')]
    assert store.sections == ['s1']


def test_clear():
    completed = {
        'locations': [{'block_id': 'one'}, {'block_id': 'two'}],
        'sections': ['s1'],
    }
    store = CompletedStore(completed)

    store.clear()

    assert store.locations == []
    assert store.sections == []
    assert store.is_dirty


def test_add_completed_location():
    store = CompletedStore()

    location = Location(block_id='one')
    store.add_completed_location(location)

    assert store.locations == [location]
    assert store.is_dirty


def test_add_completed_location_existing():
    completed = {'locations': [{'block_id': 'one'}]}
    store = CompletedStore(completed)

    location = Location(block_id='one')
    store.add_completed_location(location)

    assert len(store.locations) == 1
    assert not store.is_dirty


def test_remove_completed_location():
    completed = {'locations': [{'block_id': 'one'}]}
    store = CompletedStore(completed)

    store.remove_completed_location(Location(block_id='one'))

    assert store.locations == []
    assert store.is_dirty


def test_remove_non_existent_completed_location():
    completed = {'locations': [{'block_id': 'one'}]}
    store = CompletedStore(completed)

    store.remove_completed_location(Location(block_id='two'))

    assert len(store.locations) == 1
    assert not store.is_dirty


def test_add_completed_section():
    store = CompletedStore()

    store.add_completed_section('s1')

    assert store.sections == ['s1']
    assert store.is_dirty


def test_add_completed_section_existing():
    completed = {'sections': ['s1']}
    store = CompletedStore(completed)

    store.add_completed_section('s1')

    assert len(store.sections) == 1
    assert not store.is_dirty


def test_remove_completed_section():
    completed = {'sections': ['s1']}
    store = CompletedStore(completed)

    store.remove_completed_section('s1')

    assert store.sections == []
    assert store.is_dirty


def test_remove_non_existent_completed_section():
    completed = {'sections': ['s1']}
    store = CompletedStore(completed)

    store.remove_completed_section('s2')

    assert len(store.sections) == 1
    assert not store.is_dirty
