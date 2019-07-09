from app.questionnaire.relationship_location import RelationshipLocation


class RelationshipRouter:
    def __init__(self, block_id, list_item_ids):
        self.path = self._generate_relationships_routing_path(block_id, list_item_ids)

    def can_access_location(self, location):
        return location in self.path

    def get_first_location_url(self):
        return self.path[0].url()

    def get_last_location_url(self):
        return self.path[-1].url()

    def get_next_location_url(self, location):
        try:
            location_index = self.path.index(location)
            return self.path[location_index + 1].url()
        except IndexError:
            return None

    def get_previous_location_url(self, location):
        location_index = self.path.index(location)
        if not location_index:
            return None
        return self.path[location_index - 1].url()

    @staticmethod
    def _generate_relationships_routing_path(block_id, list_item_ids):
        path = []
        for from_item in list_item_ids:
            from_index = list_item_ids.index(from_item)
            for to_item in list_item_ids[from_index + 1 :]:
                path.append(RelationshipLocation(block_id, from_item, to_item))

        return path
