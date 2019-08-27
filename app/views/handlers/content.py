from app.questionnaire.schema_utils import transform_variants
from app.views.handlers.block import BlockHandler


class Content(BlockHandler):
    @property
    def rendered_block(self):
        return self._render_block(self.block['id'])

    def get_context(self):
        return {
            'block': self.rendered_block,
            'metadata': dict(self._questionnaire_store.metadata),
        }

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

        return self.placeholder_renderer.render(transformed_block)