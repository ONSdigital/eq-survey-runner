from flask import url_for
from app.questionnaire.location import Location
from app.questionnaire.path_finder import PathFinder
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.views.contexts.summary.group import Group
from app.questionnaire.placeholder_renderer import PlaceholderRenderer
from app.views.contexts.list_collector import build_list_items_summary_context


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

        self._placeholder_renderer = PlaceholderRenderer(
            language=self._language,
            schema=self._schema,
            answer_store=self._answer_store,
            metadata=self._metadata,
        )

    def build_groups_for_location(self, location):
        """
        Build a groups context for a particular location.

        Does not support generating multiple sections at a time (i.e. passing no list_item_id for repeating section).
        """
        section = self._schema.get_section(location.section_id)
        section_path = self._path_finder.routing_path(
            location.section_id, location.list_item_id
        )

        return [
            Group(
                group,
                section_path,
                self._answer_store,
                self._list_store,
                self._metadata,
                self._schema,
                location,
                self._language,
            ).serialize()
            for group in section['groups']
        ]

    def build_all_groups(self):
        """ NB: Does not support repeating sections """
        all_groups = []

        for section in self._schema.get_sections():
            all_groups.extend(
                self.build_groups_for_location(Location(section_id=section['id']))
            )

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

    def get_list_summaries(self, current_location):
        section = self._schema.get_section(current_location.section_id)
        visible_list_collector_blocks = self._schema.get_visible_list_blocks_for_section(
            section
        )
        section_path = self._path_finder.routing_path(
            section['id'], current_location.list_item_id
        )
        section_path_block_ids = [location.block_id for location in section_path]
        list_summaries = []

        for list_collector_block in visible_list_collector_blocks:
            add_link = url_for(
                'questionnaire.block',
                list_name=list_collector_block['for_list'],
                block_id=list_collector_block['add_block']['id'],
            )

            if list_collector_block['id'] not in section_path_block_ids:
                driving_question_block = QuestionnaireSchema.get_driving_question_for_list(
                    section, list_collector_block['for_list']
                )

                if driving_question_block:
                    add_link = url_for(
                        'questionnaire.block', block_id=driving_question_block['id']
                    )

            rendered_summary = self._placeholder_renderer.render(
                list_collector_block['summary'], current_location.list_item_id
            )

            list_summary = {
                'title': rendered_summary['title'],
                'add_link': add_link,
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

        return list_summaries

    def get_title_for_location(self, location):
        title = self._schema.get_section(location.section_id).get('title')

        if location.list_item_id:
            repeating_title = self._schema.get_repeating_title_for_section(
                location.section_id
            )
            if repeating_title:
                title = self._placeholder_renderer.render_placeholder(
                    repeating_title, location.list_item_id
                )
        return title

    def section_summary(self, current_location):
        block = self._schema.get_block(current_location.block_id)

        return {
            'summary': {
                'groups': self.build_groups_for_location(current_location),
                'answers_are_editable': True,
                'collapsible': block.get('collapsible', False),
                'summary_type': 'SectionSummary',
                'title': self.get_title_for_location(current_location),
                'list_summaries': self.get_list_summaries(current_location),
            }
        }
