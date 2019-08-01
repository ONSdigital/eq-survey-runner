from app.views.handlers.block import BlockHandler
from app.views.contexts.question import build_question_context


class Question(BlockHandler):
    def get_context(self, form):
        return build_question_context(self.rendered_block, form)

    def handle_post(self, form):
        self.questionnaire_store_updater.update_answers(form)

        self.questionnaire_store_updater.add_completed_location()

        if self.questionnaire_store_updater.is_dirty:
            section = self._schema.get_section_for_block_id(self.rendered_block['id'])
            self._routing_path = self.path_finder.routing_path(section)

        self._update_section_completeness()

        self.questionnaire_store_updater.save()
