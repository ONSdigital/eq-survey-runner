from app.views.handlers.content import Content
from app.views.contexts.summary_context import build_view_context_for_section_summary


class SectionSummary(Content):
    @property
    def rendered_block(self):
        return self._render_block(self.block['id'])

    def get_context(self, _):
        return build_view_context_for_section_summary(
            self._questionnaire_store.metadata,
            self._schema,
            self._questionnaire_store.answer_store,
            self._questionnaire_store.list_store,
            self.block['type'],
            self._current_location,
            self._language,
        )
