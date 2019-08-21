from app.views.handlers.content import Content
from app.views.contexts.calculated_summary import (
    build_view_context_for_calculated_summary,
)


class CalculatedSummary(Content):
    def get_context(self, _):
        return build_view_context_for_calculated_summary(
            self._questionnaire_store.metadata,
            self._schema,
            self._questionnaire_store.answer_store,
            self._questionnaire_store.list_store,
            self.block['type'],
            self._current_location,
        )
