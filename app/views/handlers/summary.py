from app.views.contexts.summary.block import Block
from app.views.contexts.summary_context import build_view_context_for_summary
from app.views.handlers.content import Content


def _is_view_submitted_response_enabled(schema):
    view_submitted_response = schema.get('view_submitted_response')
    if view_submitted_response:
        return view_submitted_response['enabled']

    return False


class Summary(Content):
    def __init__(self, *args):
        super().__init__(*args)

    def get_context(self):
        context = build_view_context_for_summary(
            self._schema, self.rendered_block['type'], self.path_finder
        )

        for group in context.get('summary').get('groups'):
            for block in group.get('blocks'):
                block['question'] = Block.get_question(
                    block['id'],
                    self._questionnaire_store.answer_store,
                    self._questionnaire_store.list_store,
                    self._questionnaire_store.metadata,
                    self._schema,
                    self._current_location,
                )

        context['summary'].update(
            {
                'is_view_submission_response_enabled': _is_view_submitted_response_enabled(
                    self._schema.json
                ),
                'collapsible': self.rendered_block.get('collapsible', False),
            }
        )

        return self.placeholder_renderer.render(context)
