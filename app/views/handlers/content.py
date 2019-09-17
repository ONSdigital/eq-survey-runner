from app.questionnaire.schema_utils import transform_variants
from app.views.handlers.block import BlockHandler
from app.helpers.template_helper import safe_content

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

        self.page_title = self._get_page_title(transformed_block)

        return self.placeholder_renderer.render(
            transformed_block, self._current_location.list_item_id
        )

    def _get_page_title(self, transformed_block):
        if 'content' in transformed_block:
            if type(transformed_block['content']['title']) is str:
                content_title = transformed_block['content']['title']
            else:
                content_title = transformed_block['content']['title']['text']

            page_title = '{content_title} - {survey_title}'.format(
                content_title=content_title, survey_title=self._schema.json['title']
            )

            return safe_content(page_title)

