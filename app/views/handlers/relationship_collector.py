from app.questionnaire.location import Location
from app.questionnaire.relationship_router import RelationshipRouter
from app.views.handlers.question import Question


class RelationshipCollector(Question):
    def __init__(self, *args):
        self._relationship_router = None
        super().__init__(*args)

    @property
    def relationship_router(self):
        if not self._relationship_router:
            block_id = self._current_location.block_id
            section_id = self._current_location.section_id
            list_items = self._questionnaire_store.list_store[
                self._schema.get_block(block_id)['for_list']
            ].items
            relationship_router = RelationshipRouter(
                section_id=section_id, block_id=block_id, list_item_ids=list_items
            )
            self._relationship_router = relationship_router
        return self._relationship_router

    def is_location_valid(self):
        if isinstance(self._current_location, Location):
            return self.router.can_access_location(
                self._current_location, self._routing_path
            )

        parent_location = Location(
            section_id=self._current_location.section_id,
            block_id=self._current_location.block_id,
        )
        can_access_parent_location = self.router.can_access_location(
            parent_location, self._routing_path
        )
        can_access_relationship_location = self.relationship_router.can_access_location(
            self._current_location
        )
        if not can_access_parent_location or not can_access_relationship_location:
            return False
        return True

    def get_first_location_url(self):
        return self.relationship_router.get_first_location_url()

    def get_previous_location_url(self):
        previous_location_url = self.relationship_router.get_previous_location_url(
            self._current_location
        )
        if not previous_location_url:
            parent_location = Location(
                section_id=self._current_location.section_id, block_id=self.block['id']
            )
            previous_location_url = self.router.get_previous_location_url(
                parent_location, self._routing_path
            )
        return previous_location_url

    def get_next_location_url(self):
        next_location_url = self.relationship_router.get_next_location_url(
            self._current_location
        )
        if next_location_url:
            return next_location_url

        parent_location = Location(
            section_id=self._current_location.section_id, block_id=self.block['id']
        )
        return self.router.get_next_location_url(parent_location, self._routing_path)

    def save_on_sign_out(self):
        self.questionnaire_store_updater.update_relationship_answer(
            self.form.data,
            self._current_location.list_item_id,
            self._current_location.to_list_item_id,
        )

        parent_location = Location(
            section_id=self._current_location.section_id,
            block_id=self.rendered_block['id'],
        )
        self.questionnaire_store_updater.remove_completed_location(parent_location)

        self.questionnaire_store_updater.save()

    def handle_post(self):
        self.questionnaire_store_updater.update_relationship_answer(
            self.form.data,
            self._current_location.list_item_id,
            self._current_location.to_list_item_id,
        )

        if self._is_last_relationship():
            parent_location = Location(
                section_id=self._current_location.section_id,
                block_id=self.rendered_block['id'],
            )
            self.questionnaire_store_updater.add_completed_location(
                location=parent_location
            )
            self._update_section_completeness(location=parent_location)

        self.questionnaire_store_updater.save()

    def _is_last_relationship(self):
        if self.relationship_router.get_next_location_url(self._current_location):
            return False
        return True
