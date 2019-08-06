from app.data_model.relationship_store import Relationship, RelationshipStore

relationships = [
    {
        'list_item_id': '123456',
        'to_list_item_id': '789101',
        'relationship': 'Husband or Wife',
    },
    {
        'list_item_id': '123456',
        'to_list_item_id': 'ghijkl',
        'relationship': 'Husband or Wife',
    },
]


def test_serialisation():
    relationship_store = RelationshipStore(relationships)

    assert relationship_store.serialise() == relationships


def test_deserialisation():
    relationship_store = RelationshipStore(relationships)

    assert Relationship(**relationships[0]) in relationship_store
    assert len(relationship_store) == 2


def test_clear():  # pylint: disable=redefined-outer-name
    relationship_store = RelationshipStore(relationships)
    relationship_store.clear()

    assert not relationship_store
    assert relationship_store.is_dirty


def test_add_relationship():
    relationship = Relationship(**relationships[0])

    relationship_store = RelationshipStore()
    relationship_store.add_or_update(relationship)

    assert (
        relationship_store.get_relationship(
            relationship.list_item_id, relationship.to_list_item_id
        )
        == relationship
    )
    assert len(relationship_store) == 1
    assert relationship_store.is_dirty


def test_add_relationship_that_already_exists():
    relationship = relationships[0]
    relationship_store = RelationshipStore([relationship])
    relationship_store.add_or_update(Relationship(**relationship))

    assert len(relationship_store) == 1
    assert not relationship_store.is_dirty


def test_get_relationship():
    relationship_store = RelationshipStore(relationships)
    relationship = relationship_store.get_relationship(
        list_item_id='123456', to_list_item_id='789101'
    )
    assert relationship


def test_get_relationship_that_doesnt_exist():
    relationship_store = RelationshipStore(relationships)
    relationship = relationship_store.get_relationship(
        list_item_id='123456', to_list_item_id='yyyyyy'
    )
    assert not relationship


def test_remove_id_in_multiple_relationships():
    relationship_store = RelationshipStore(relationships)
    relationship_store.remove_all_relationships_for_list_item_id('123456')

    assert not relationship_store
    assert relationship_store.is_dirty


def test_remove_id_in_single_relationship():
    relationship_store = RelationshipStore(relationships)
    relationship_store.remove_all_relationships_for_list_item_id('789101')
    remaining_relationship = Relationship(**relationships[1])

    assert len(relationship_store) == 1
    assert (
        relationship_store.get_relationship(
            remaining_relationship.list_item_id, remaining_relationship.to_list_item_id
        )
        == remaining_relationship
    )
    assert relationship_store.is_dirty


def test_update_existing_relationship():
    relationship_store = RelationshipStore(relationships)

    relationship = Relationship(**relationships[0])
    relationship.relationship = 'test'

    relationship_store.add_or_update(relationship)

    assert len(relationship_store) == 2
    updated_relationship = relationship_store.get_relationship(
        relationship.list_item_id, relationship.to_list_item_id
    )
    assert updated_relationship.relationship == 'test'
    assert relationship_store.is_dirty
