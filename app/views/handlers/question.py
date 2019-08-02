from app.data_model.section_location import SectionLocation
from app.views.handlers.block import BlockHandler
from app.views.contexts.question import build_question_context


class Question(BlockHandler):
    def get_context(self, form):
        return build_question_context(self.rendered_block, form)

    def handle_post(self, form):
        self.questionnaire_store_updater.update_answers(form)

        if self.questionnaire_store_updater.is_dirty:
            section_id = self._schema.get_section_id_for_block_id(
                self._current_location.block_id
            )
            section_location = SectionLocation(
                section_id, self._current_location.list_item_id
            )

            self._routing_path = self.path_finder.routing_path(section_location)

        self.questionnaire_store_updater.add_completed_location()
        self._update_section_completeness()

        self.questionnaire_store_updater.save()
