from app.views.contexts.question import build_question_context
from app.views.handlers.block import BlockHandler


class Question(BlockHandler):
    def get_context(self, form):
        return build_question_context(self.rendered_block, form)

    def handle_post(self, form):
        self.questionnaire_store_updater.update_answers(form)

        self.questionnaire_store_updater.add_completed_location()

        if self.questionnaire_store_updater.is_dirty:
            self._routing_path = self.path_finder.routing_path(
                section_id=self._current_location.section_id,
                list_item_id=self._current_location.list_item_id,
            )

        self._update_section_completeness()

        self.questionnaire_store_updater.save()
