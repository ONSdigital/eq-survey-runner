from flask import url_for

from app.views.contexts.list_collector import build_list_items_summary_context
from app.views.handlers.summary import Summary


class SectionSummary(Summary):
    @property
    def rendered_block(self):
        return self._render_block(self.block['id'])

    def get_context(self):
        group = self._schema.get_group_for_block_id(self._current_location.block_id)
        section = self._schema.get_section(group['parent_id'])

        context = self.build_context([section])
        context = self.add_questions_to_blocks(context)

        list_collector_blocks = self._schema.get_visible_list_blocks_for_section(
            section
        )

        list_summaries = []

        for list_collector_block in list_collector_blocks:
            rendered_summary = self.placeholder_renderer.render(
                list_collector_block['summary']
            )

            list_summary = {
                'title': rendered_summary['title'],
                'add_link': url_for(
                    'questionnaire.block',
                    list_name=list_collector_block['for_list'],
                    block_id=list_collector_block['add_block']['id'],
                ),
                'add_link_text': rendered_summary['add_link_text'],
                'empty_list_text': rendered_summary['empty_list_text'],
                'list_items': build_list_items_summary_context(
                    list_collector_block,
                    self._schema,
                    self._questionnaire_store.answer_store,
                    self._questionnaire_store.list_store,
                    self._language,
                ),
                'list_name': list_collector_block['for_list'],
            }
            list_summaries.append(list_summary)

        context['summary'].update(
            {'title': section.get('title'), 'list_summaries': list_summaries}
        )

        return context
