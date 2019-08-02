from app.data_model.section_location import SectionLocation
from app.views.handlers.block import BlockHandler
from app.views.contexts.question import build_question_context
from app.questionnaire.location import Location


class PrimaryPersonQuestion(BlockHandler):
    @property
    def parent_location(self):
        return Location(self.rendered_block['parent_id'])

    def is_location_valid(self):
        return self.router.can_access_location(self.parent_location, self._routing_path)

    def get_previous_location_url(self):
        return self.parent_location.url()

    def get_next_location_url(self):
        return self.router.get_next_location_url(
            self.parent_location, self._routing_path
        )

    def get_context(self, form):
        return build_question_context(self.rendered_block, form)

    def handle_post(self, form):
        self.questionnaire_store_updater.update_answers(form)
        parent_section_id = self._schema.get_section_for_block_id(
            self.parent_location.block_id
        )['id']

        section_location = SectionLocation(
            parent_section_id, self.parent_location.list_item_id
        )

        self.questionnaire_store_updater.add_completed_location(
            section_location=section_location, location=self.parent_location
        )
        self._update_section_completeness(section_location=section_location)
        self.questionnaire_store_updater.save()
