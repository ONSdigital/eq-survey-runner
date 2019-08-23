from app.views.contexts.summary_context import SummaryContext
from app.views.handlers.content import Content


class Summary(Content):
    def __init__(self, *args):
        super().__init__(*args)

    def get_context(self):
        summary_context = SummaryContext(
            self._language,
            self._schema,
            self._questionnaire_store.answer_store,
            self._questionnaire_store.list_store,
            self._questionnaire_store.metadata,
            self._current_location,
        )
        return summary_context.summary()
