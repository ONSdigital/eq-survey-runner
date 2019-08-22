from app.questionnaire.path_finder import PathFinder
from app.views.contexts.summary.group import Group
from app.questionnaire.placeholder_renderer import PlaceholderRenderer


class SummaryContext:
    def __init__(self, language, schema, answer_store, list_store, metadata, current_location):
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
            self._block_type = self._schema.get_block(self._current_location.block_id)[
                'type'
            ]
        else:
            self._block_type = 'Summary'

    def _build_groups_for_section(self, section_id, list_item_id=None, section=None):
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

    def _build_all_groups(self):
        all_groups = []

        for section in self._schema.get_sections():
            section_id = section['id']

            repeating_list = self._schema.get_repeating_list_for_section(section_id)

            if repeating_list:
                for list_item_id in self._list_store[repeating_list].items:
                    all_groups.extend(
                        self._build_groups_for_section(section_id, list_item_id)
                    )
            else:
                all_groups.extend(self._build_groups_for_section(section_id))

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
                ).get('collapsible', False)
            }
        )

        return context

    def summary(self, section_id=None, list_item_id=None, section=None):
        if section_id or list_item_id:
            groups = self._build_groups_for_section(section_id, list_item_id)
        elif section:
            groups = self._build_groups_for_section(section['id'], section=section)
        else:
            groups = self._build_all_groups()

        context = {
            'summary': {
                'groups': groups,
                'answers_are_editable': True,
                'summary_type': self._block_type,
            }
        }
        return context

    def section_summary(self):
        section_id = self._current_location.section_id
        list_item_id = self._current_location.list_item_id

        context = self.summary(section_id, list_item_id)

        title = self._schema.get_section(section_id).get('title')

        if list_item_id:

            repeating_title = self._schema.get_repeating_title_for_section(section_id)

            if repeating_title:
                placeholder_renderer = PlaceholderRenderer(
                    language=self._language,
                    schema=self._schema,
                    answer_store=self._answer_store,
                    metadata=self._metadata,
                    list_item_id=list_item_id,
                )
                title = placeholder_renderer.render(repeating_title)

        context['summary'].update({'title': title})
        return context


def _is_view_submitted_response_enabled(schema):
    view_submitted_response = schema.get('view_submitted_response')
    if view_submitted_response:
        return view_submitted_response['enabled']

    return False
