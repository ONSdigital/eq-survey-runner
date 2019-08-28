from flask import url_for
from app.questionnaire.path_finder import PathFinder
from app.views.contexts.summary.group import Group
from app.questionnaire.placeholder_renderer import PlaceholderRenderer
from app.views.contexts.list_collector import build_list_items_summary_context


class SummaryContext:
    def __init__(
        self, language, schema, answer_store, list_store, metadata, current_location
    ):
        self._language = language
        self._answer_store = answer_store
        self._list_store = list_store
        self._metadata = metadata
        self._schema = schema
        self._current_location = current_location
        self._path_finder = PathFinder(
            self._schema,
            self._answer_store,
            self._metadata,
            list_store=self._list_store,
        )
        if current_location:
            self._block = self._schema.get_block(self._current_location.block_id)
            self._block_type = self._block['type']
        else:
            self.block = None
            self._block_type = 'Summary'

    def build_groups_for_section(self, section_id, list_item_id=None, section=None):
        """
        Build a groups context for a particular section and list_item_id.

        Does not support generating multiple sections at a time (i.e. passing no list_item_id for repeating section).
        """
        section = section or self._schema.get_section(section_id)
        section_path = self._path_finder.routing_path(section_id, list_item_id)

        return [
            Group(
                group,
                section_path,
                self._answer_store,
                self._list_store,
                self._metadata,
                self._schema,
                self._current_location,
            ).serialize()
            for group in section['groups']
        ]

    def build_all_groups(self):
        """ NB: Does not support repeating sections (final summary and view submission)"""
        all_groups = []

        for section in self._schema.get_sections():
            section_id = section['id']

            all_groups.extend(self.build_groups_for_section(section_id))

        return all_groups

    def final_summary(self):
        context = self.summary()

        context['summary'].update(
            {
                'is_view_submission_response_enabled': _is_view_submitted_response_enabled(
                    self._schema.json
                ),
                'collapsible': self._schema.get_block(
                    self._current_location.block_id
                ).get('collapsible', False),
            }
        )

        return context

    def summary(self, section_id=None, list_item_id=None, section=None):
        if section_id or list_item_id:
            groups = self.build_groups_for_section(section_id, list_item_id)
        elif section:
            groups = self.build_groups_for_section(section['id'], section=section)
        else:
            groups = self.build_all_groups()

        context = {
            'summary': {
                'groups': groups,
                'answers_are_editable': True,
                'collapsible': self._block.get('collapsible', False),
                'summary_type': self._block_type,
            }
        }
        return context

    def section_summary(self):
        section_id = self._current_location.section_id
        section = self._schema.get_section(self._current_location.section_id)
        list_item_id = self._current_location.list_item_id

        context = self.summary(section_id, list_item_id)

        title = self._schema.get_section(section_id).get('title')

        placeholder_renderer = PlaceholderRenderer(
            language=self._language,
            schema=self._schema,
            answer_store=self._answer_store,
            metadata=self._metadata,
        )

        if list_item_id:

            repeating_title = self._schema.get_repeating_title_for_section(section_id)
            if repeating_title:
                title = placeholder_renderer.render_placeholder(repeating_title, list_item_id)

        list_collector_blocks = self._schema.get_visible_list_blocks_for_section(
            section
        )

        list_summaries = []

        for list_collector_block in list_collector_blocks:
            rendered_summary = placeholder_renderer.render(
                list_collector_block['summary'], list_item_id
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
                    self._answer_store,
                    self._list_store,
                    self._language,
                ),
                'list_name': list_collector_block['for_list'],
            }
            list_summaries.append(list_summary)

        context['summary'].update({'title': title, 'list_summaries': list_summaries})

        return context


def _is_view_submitted_response_enabled(schema):
    view_submitted_response = schema.get('view_submitted_response')
    if view_submitted_response:
        return view_submitted_response['enabled']

    return False
