from app.views.handlers.block import BlockHandler
from app.views.contexts.summary_context import build_view_context_for_final_summary


class Summary(BlockHandler):
    def get_context(self, _):
        return build_view_context_for_final_summary(
            self._questionnaire_store.metadata,
            self._schema,
            self._questionnaire_store.answer_store,
            self._questionnaire_store.list_store,
            self.rendered_block['type'],
            self.rendered_block,
        )
