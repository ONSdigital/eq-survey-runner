from typing import List, Mapping

from copy import deepcopy
from app.views.contexts.summary.block import Block
from app.views.contexts.summary_context import build_group_summary_context

from app.views.contexts.summary_context import SummaryContext
from app.views.handlers.content import Content


def _is_view_submitted_response_enabled(schema):
    view_submitted_response = schema.get('view_submitted_response')
    if view_submitted_response:
        return view_submitted_response['enabled']

    return False


class Summary(Content):
    def add_questions_to_blocks(self, context):
        updated_context = deepcopy(context)

        for group in updated_context.get('summary').get('groups'):
            for block in group.get('blocks'):
                block['question'] = Block.get_question(
                    block['id'],
                    self._questionnaire_store.answer_store,
                    self._questionnaire_store.list_store,
                    self._questionnaire_store.metadata,
                    self._schema,
                    self._current_location,
                )
        return updated_context

    def build_context(self, sections: List[Mapping] = None):
        summary_rendering_context = build_group_summary_context(
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

        summary_context = SummaryContext(
            self._language,
            self._schema,
            self._questionnaire_store.answer_store,
            self._questionnaire_store.list_store,
            self._questionnaire_store.metadata,
        )
        collapsible = self._schema.get_block(self._current_location.block_id).get(
            'collapsible', False
        )
        return summary_context.summary(collapsible)
