from app.views.handlers.question import Question
from app.views.contexts.question import build_question_context
from app.questionnaire.location import Location


class PrimaryPersonQuestion(Question):
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
        self.questionnaire_store_updater.add_completed_location(
            location=self.parent_location, section_id=parent_section_id
        )
        self._update_section_completeness()
        self.questionnaire_store_updater.save()
