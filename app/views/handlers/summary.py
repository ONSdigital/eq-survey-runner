from app.views.handlers.block import BlockHandler
from app.views.contexts.summary_context import build_view_context_for_final_summary


class Summary(BlockHandler):
    def get_context(self, _):
        return build_view_context_for_final_summary(
            schema=self._schema,
            answer_store=self._questionnaire_store.answer_store,
            list_store=self._questionnaire_store.list_store,
            metadata=self._questionnaire_store.metadata,
            rendered_block=self.rendered_block,
            current_location=self.current_location,
        )
