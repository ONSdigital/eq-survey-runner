from app.views.handlers.block import BlockHandler
from app.views.contexts.summary_context import build_view_context_for_calculated_summary


class CalculatedSummary(BlockHandler):
    def get_context(self, _):
        return build_view_context_for_calculated_summary(
            self._questionnaire_store.metadata,
            self._schema,
            self._questionnaire_store.answer_store,
            self._questionnaire_store.list_store,
            self.rendered_block['type'],
            self._current_location,
        )
