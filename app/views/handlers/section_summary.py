from app.views.handlers.content import Content
from app.views.contexts.summary_context import SummaryContext


class SectionSummary(Content):
    @property
    def rendered_block(self):
        return self._render_block(self.block['id'])

    def get_context(self):
        summary_context = SummaryContext(
            self._language,
            self._schema,
            self._questionnaire_store.answer_store,
            self._questionnaire_store.list_store,
            self._questionnaire_store.metadata,
        )
        return summary_context.section_summary(self._current_location)
