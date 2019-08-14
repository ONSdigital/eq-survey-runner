from werkzeug.utils import cached_property

from app.questionnaire.placeholder_renderer import PlaceholderRenderer
from app.questionnaire.questionnaire_store_updater import QuestionnaireStoreUpdater
from app.questionnaire.schema_utils import transform_variants
from app.views.handlers.block import BlockHandler
from app.views.contexts.question import build_question_context


class Question(BlockHandler):
    @cached_property
    def rendered_block(self):
        return self._render_block(self.block['id'])

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

    @cached_property
    def questionnaire_store_updater(self):
        if not self._questionnaire_store_updater:
            self._questionnaire_store_updater = QuestionnaireStoreUpdater(
                self._current_location,
                self._schema,
                self._questionnaire_store,
                self.rendered_block.get('question'),
            )
        return self._questionnaire_store_updater

    def _render_block(self, block_id):
        block_schema = self._schema.get_block(block_id)

        transformed_block = transform_variants(
            block_schema,
            self._schema,
            self._questionnaire_store.metadata,
            self._questionnaire_store.answer_store,
            self._questionnaire_store.list_store,
            self._current_location,
        )

        placeholder_renderer = PlaceholderRenderer(
            language=self._language,
            answer_store=self._questionnaire_store.answer_store,
            metadata=self._questionnaire_store.metadata,
        )

        rendered_question = placeholder_renderer.render(
            transformed_block.pop('question')
        )
        return {**transformed_block, **{'question': rendered_question}}
