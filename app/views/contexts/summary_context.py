from typing import List, Mapping

from flask import url_for
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.questionnaire.location import Location
from app.questionnaire.path_finder import PathFinder
from app.views.contexts.summary.group import Group
from app.questionnaire.placeholder_renderer import PlaceholderRenderer
from app.views.contexts.list_collector import build_list_items_summary_context


def get_section_context(section, block_ids_to_filter) -> List:
    group_collection = []

    for group_schema in section['groups']:
        blocks_to_return = []
        for block in group_schema['blocks']:
            if block['id'] in block_ids_to_filter and block['type'] == 'Question':
                blocks_to_return.append(
                    {
                        'id': block['id'],
                        'title': block.get('title'),
                        'number': block.get('number'),
                        'link': url_for('questionnaire.block', block_id=block['id']),
                    }
                )
        group_collection.append(
            {
                'id': group_schema['id'],
                'title': group_schema.get('title'),
                'blocks': blocks_to_return,
            }
        )

    return group_collection


def build_group_summary_context(
    schema: QuestionnaireSchema, path_finder: PathFinder, sections: List[Mapping] = None
) -> List:
    sections = sections or schema.get_sections()
    paths = [path_finder.routing_path(section['id']) for section in sections]

    group_collection = []

    for path, section in zip(paths, sections):
        block_ids_on_path = [location.block_id for location in path]
        group_collection.extend(get_section_context(section, block_ids_on_path))
    return group_collection


class SummaryContext:
    def __init__(self, language, schema, answer_store, list_store, metadata):
        self._language = language
        self._answer_store = answer_store
        self._list_store = list_store
        self._metadata = metadata
        self._schema = schema
        self._path_finder = PathFinder(
            self._schema,
            self._answer_store,
            self._metadata,
            list_store=self._list_store,
        )

    def build_groups_for_section(self, section_id, list_name=None, list_item_id=None):
        """
        Build a groups context for a particular section and list_item_id.

        Does not support generating multiple sections at a time (i.e. passing no list_item_id for repeating section).
        """
        section = self._schema.get_section(section_id)
        section_path = self._path_finder.routing_path(section_id, list_item_id)

        location = Location(section_id, list_name=list_name, list_item_id=list_item_id)

        return [
            Group(
                group,
                section_path,
                self._answer_store,
                self._list_store,
                self._metadata,
                self._schema,
                location,
            ).serialize()
            for group in section['groups']
        ]

    def build_all_groups(self):
        """ NB: Does not support repeating sections """
        all_groups = []

        for section in self._schema.get_sections():
            section_id = section['id']

            all_groups.extend(self.build_groups_for_section(section_id))

        return all_groups

    def summary(self, collapsible):
        groups = self.build_all_groups()

        context = {
            'summary': {
                'groups': groups,
                'answers_are_editable': True,
                'collapsible': collapsible,
                'summary_type': 'Summary',
            }
        }
        return context

    def section_summary(self, current_location):
        section_id = current_location.section_id
        section = self._schema.get_section(current_location.section_id)
        list_item_id = current_location.list_item_id
        list_name = current_location.list_name
        block = self._schema.get_block(current_location.block_id)

        groups = self.build_groups_for_section(section_id, list_name, list_item_id)

        context = {
            'summary': {
                'groups': groups,
                'answers_are_editable': True,
                'collapsible': block.get('collapsible', False),
                'summary_type': 'SectionSummary',
            }
        }

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
                title = placeholder_renderer.render_placeholder(
                    repeating_title, list_item_id
                )

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
