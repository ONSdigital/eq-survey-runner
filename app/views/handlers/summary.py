from typing import List, Mapping

from app.views.contexts.summary.block import Block
from app.views.contexts.summary_context import build_summary_rendering_context
from app.views.handlers.content import Content


def _is_view_submitted_response_enabled(schema):
    view_submitted_response = schema.get('view_submitted_response')
    if view_submitted_response:
        return view_submitted_response['enabled']

    return False


class Summary(Content):
    def add_context_questions(self, context):
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

    def build_context(self, sections: List[Mapping] = None):
        summary_rendering_context = build_summary_rendering_context(
            self._schema, self.path_finder, sections
        )

        return {
            'summary': {
                'groups': summary_rendering_context,
                'answers_are_editable': True,
                'summary_type': self.rendered_block['type'],
            }
        }

    def get_context(self):
        context = self.build_context()

        self.add_context_questions(context)

        context['summary'].update(
            {
                'is_view_submission_response_enabled': _is_view_submitted_response_enabled(
                    self._schema.json
                ),
                'collapsible': self.rendered_block.get('collapsible', False),
            }
        )

        return self.placeholder_renderer.render(context)
