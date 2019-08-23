from app.views.contexts.summary.block import Block
from app.views.handlers.content import Content
from app.views.contexts.summary_context import build_view_context_for_summary


class SectionSummary(Content):
    @property
    def rendered_block(self):
        return self._render_block(self.block['id'])

    def get_context(self):
        group = self._schema.get_group_for_block_id(self._current_location.block_id)
        section = self._schema.get_section(group['parent_id'])

        context = build_view_context_for_summary(
            self._schema, self.block['type'], self.path_finder, [section]
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

        context['summary'].update({'title': section.get('title')})

        return context
