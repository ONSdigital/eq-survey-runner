from app.views.contexts.summary_context import build_view_context_for_final_summary
from app.views.handlers.content import Content


class Summary(Content):
    def __init__(self, *args):
        super().__init__(*args)

    def get_context(self, _):
        return build_view_context_for_final_summary(
            metadata=self._questionnaire_store.metadata,
            schema=self._schema,
            answer_store=self._questionnaire_store.answer_store,
            list_store=self._questionnaire_store.list_store,
            rendered_block=self.rendered_block,
            current_location=self.current_location,
        )
