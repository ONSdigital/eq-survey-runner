from dataclasses import dataclass, asdict
from typing import List, Mapping, Optional


@dataclass
class Relationship:
    """
    Represents a relationship between two items.
    """

    from_list_item_id: str
    to_list_item_id: str
    relationship: str

    def for_json(self) -> Mapping:
        return asdict(self)


class RelationshipStore:
    """
    Stores and updates relationships.
    """

    def __init__(self, relationships: Optional[List[Mapping]] = None) -> None:
        self._is_dirty = False
        self._relationships = self._build_map(relationships or [])

    def __iter__(self):
        return iter(self._relationships.values())

    def __contains__(self, relationship):
        return (
            relationship.from_list_item_id,
            relationship.to_list_item_id,
        ) in self._relationships

    def __len__(self):
        return len(self._relationships)

    @property
    def is_dirty(self):
        return self._is_dirty

    def clear(self):
        self._relationships.clear()
        self._is_dirty = True

    def serialise(self):
        return [
            relationship.for_json() for relationship in self._relationships.values()
        ]

    def get_relationship(self, from_list_item_id, to_list_item_id):
        key = (from_list_item_id, to_list_item_id)
        return self._relationships.get(key)

    def add_or_update(self, relationship: Relationship):
        key = (relationship.from_list_item_id, relationship.to_list_item_id)

        existing_relationship = self._relationships.get(key)

        if existing_relationship != relationship:
            self._is_dirty = True
            self._relationships[key] = relationship

    def remove_all_relationships_for_list_item_id(self, list_item_id: str):
        """Remove all relationships associated with a particular list_item_id
        This method iterates through the entire list of relationships.
        """

        keys_to_delete = []

        for relationship in self:
            if list_item_id in (
                relationship.to_list_item_id,
                relationship.from_list_item_id,
            ):
                keys_to_delete.append(
                    (relationship.from_list_item_id, relationship.to_list_item_id)
                )

        for key in keys_to_delete:
            del self._relationships[key]
            self._is_dirty = True

    @staticmethod
    def _build_map(relationships):
        return {
            (
                relationship['from_list_item_id'],
                relationship['to_list_item_id'],
            ): Relationship(**relationship)
            for relationship in relationships
        }
