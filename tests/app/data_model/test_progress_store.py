from app.data_model.progress import Progress
from app.data_model.progress_store import ProgressStore, CompletionStatus
from app.questionnaire.location import Location


def test_serialisation():
    store = ProgressStore()

    store.add_completed_location('s1', Location('one'))
    store.add_completed_location('s1', Location('two'))
    store.update_section_status('s1', CompletionStatus.COMPLETED)

    serialised = store.serialise()

    assert serialised == [
        Progress.from_dict(
            {
                'section_id': 's1',
                'list_item_id': None,
                'status': CompletionStatus.COMPLETED,
                'locations': [{'block_id': 'one'}, {'block_id': 'two'}],
            }
        )
    ]


def test_deserialisation():
    in_progress_sections = [
        {
            'section_id': 's1',
            'list_item_id': None,
            'status': CompletionStatus.IN_PROGRESS,
            'locations': [{'block_id': 'one'}, {'block_id': 'two'}],
        }
    ]
    store = ProgressStore(in_progress_sections)

    assert store.get_section_status('s1') == CompletionStatus.IN_PROGRESS
    assert store.get_completed_locations('s1') == [
        Location(block_id='one'),
        Location(block_id='two'),
    ]


def test_clear():
    in_progress_sections = [
        {
            'section_id': 's1',
            'list_item_id': None,
            'status': CompletionStatus.COMPLETED,
            'locations': [{'block_id': 'one'}, {'block_id': 'two'}],
        }
    ]
    store = ProgressStore(in_progress_sections)

    store.clear()

    assert store.serialise() == []
    assert store.is_dirty


def test_add_completed_location():
    store = ProgressStore()

    location = Location(block_id='one')
    store.add_completed_location('s1', location)

    assert store.get_completed_locations('s1') == [location]
    assert store.is_dirty


def test_add_completed_location_existing():
    completed = [
        {
            'section_id': 's1',
            'list_item_id': None,
            'status': CompletionStatus.COMPLETED,
            'locations': [{'block_id': 'one'}],
        }
    ]
    store = ProgressStore(completed)

    location = Location(block_id='one')
    store.add_completed_location('s1', location)

    assert store.get_section_status('s1') == CompletionStatus.COMPLETED
    assert len(store.get_completed_locations('s1')) == 1
    assert not store.is_dirty


def test_add_completed_location_new():
    completed = [
        {
            'section_id': 's1',
            'list_item_id': None,
            'status': CompletionStatus.COMPLETED,
            'locations': [{'block_id': 'one'}],
        }
    ]
    store = ProgressStore(completed)

    location = Location(block_id='two')
    store.add_completed_location('s1', location)

    assert store.get_section_status('s1') == CompletionStatus.COMPLETED
    assert len(store.get_completed_locations('s1')) == 2
    assert store.is_dirty


def test_remove_completed_location():
    completed = [
        {
            'section_id': 's1',
            'list_item_id': None,
            'status': CompletionStatus.COMPLETED,
            'locations': [{'block_id': 'one'}, {'block_id': 'two'}],
        }
    ]
    store = ProgressStore(completed)

    store.remove_completed_location('s1', Location(block_id='two'))

    assert store.get_completed_locations('s1') == [Location(block_id='one')]
    assert store.is_dirty


def test_remove_final_completed_location_removes_section():
    completed = [
        {
            'section_id': 's1',
            'list_item_id': None,
            'status': CompletionStatus.COMPLETED,
            'locations': [{'block_id': 'one'}],
        }
    ]
    store = ProgressStore(completed)

    store.remove_completed_location('s1', Location(block_id='one'))

    assert 's1' not in store
    assert store.is_dirty


def test_remove_non_existent_completed_location():
    completed = [
        {
            'section_id': 's1',
            'list_item_id': None,
            'status': CompletionStatus.COMPLETED,
            'locations': [{'block_id': 'one'}],
        }
    ]
    store = ProgressStore(completed)

    store.remove_completed_location('s1', Location(block_id='two'))

    assert len(store.get_completed_locations('s1')) == 1
    assert not store.is_dirty


def test_update_section_status():
    completed = [
        {
            'section_id': 's1',
            'list_item_id': None,
            'status': CompletionStatus.COMPLETED,
            'locations': [{'block_id': 'one'}],
        }
    ]
    store = ProgressStore(completed)

    store.update_section_status('s1', CompletionStatus.IN_PROGRESS)

    assert store.get_section_status('s1') == CompletionStatus.IN_PROGRESS
    assert store.is_dirty


def test_update_non_existing_section_status():
    completed = [
        {
            'section_id': 's1',
            'list_item_id': None,
            'status': CompletionStatus.COMPLETED,
            'locations': [{'block_id': 'one'}],
        }
    ]
    store = ProgressStore(completed)

    store.update_section_status('s2', CompletionStatus.IN_PROGRESS)

    assert store.get_section_status('s1') == CompletionStatus.COMPLETED
    assert 's2' not in store
    assert not store.is_dirty


def test_get_section_status():
    completed = [
        {
            'section_id': 's1',
            'list_item_id': None,
            'status': CompletionStatus.COMPLETED,
            'locations': [{'block_id': 'one'}],
        }
    ]
    store = ProgressStore(completed)

    assert store.get_section_status('s1') == CompletionStatus.COMPLETED


def test_get_section_locations():
    completed = [
        {
            'section_id': 's1',
            'list_item_id': None,
            'status': CompletionStatus.COMPLETED,
            'locations': [{'block_id': 'one'}],
        }
    ]
    store = ProgressStore(completed)

    assert store.get_completed_locations('s1') == [Location(block_id='one')]


def test_completed_section_ids():
    completed = [
        {
            'section_id': 's1',
            'list_item_id': None,
            'status': CompletionStatus.COMPLETED,
            'locations': [{'block_id': 'one'}, {'block_id': 'two'}],
        },
        {
            'section_id': 's2',
            'list_item_id': None,
            'status': CompletionStatus.IN_PROGRESS,
            'locations': [{'block_id': 'three'}],
        },
    ]
    store = ProgressStore(completed)

    assert store.completed_sections == [('s1', None)]
