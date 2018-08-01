from collections import defaultdict

from structlog import get_logger

from app.questionnaire.completeness import Completeness
from app.questionnaire.location import Location
from app.questionnaire.rules import evaluate_repeat, get_answer_ids_on_routing_path

logger = get_logger()


class Navigation:
    """
    Reads navigation config from the schema and returns collections of dicts that describe
    completion status of each group
    """
    def __init__(
            self,
            schema,
            answer_store,
            metadata,
            completed_blocks,
            routing_path,
            completeness):
        self.schema = schema
        self.metadata = metadata
        self.answer_store = answer_store
        self.completed_blocks = completed_blocks
        self.routing_path = routing_path
        self.completeness = completeness

    def build_navigation(self, current_group_id, current_group_instance):
        """
        Build navigation based on the current group/instance selected

        :param current_group_id:
        :param current_group_instance:
        :return:
        """
        navigation_block = self.schema.json.get('navigation')
        if navigation_block is None or navigation_block.get('visible', True) is False:
            return None

        navigation = []

        for section in self.schema.sections:
            non_skipped_groups = self._get_non_skipped_groups(section)
            if not non_skipped_groups:
                continue

            target_location = self._get_location_for_section(section, non_skipped_groups)

            # if the first group in a section is a repeating group then repeat the section
            # navigation link for each repeat instead of rendering the section title
            repeating_rule = None
            if len(non_skipped_groups) == 1:
                repeating_rule = self.schema.get_repeat_rule(non_skipped_groups[0])

            if repeating_rule:
                navigation.extend(self._build_repeating_navigation(repeating_rule, section, current_group_id,
                                                                   current_group_instance))
            else:
                navigation.append(
                    self._build_single_navigation(
                        section, current_group_id, target_location))

        return navigation

    def _get_non_skipped_groups(self, section):
        return [
            group for group in section['groups']
            if self.completeness.get_state_for_group(group) != Completeness.SKIPPED
        ]

    def _build_single_navigation(self, section, current_group_id, first_location):
        group_ids = (group['id'] for group in section['groups'])
        is_highlighted = current_group_id in group_ids
        is_completed = self.completeness.is_section_complete(section)

        return self._generate_item(section['title'], is_completed, first_location, is_highlighted)

    def _build_repeating_navigation(self, repeating_rule, section, current_group_id, current_group_instance):
        groups = section['groups']
        answer_ids_on_path = get_answer_ids_on_routing_path(self.schema, self.routing_path)
        no_of_repeats = evaluate_repeat(repeating_rule, self.answer_store, answer_ids_on_path)

        repeating_nav = []
        if repeating_rule['type'] == 'answer_count':
            link_names = self._generate_link_names(section['title_from_answers'])

            for group in groups:
                is_current_group = group['id'] == current_group_id
                repeating_nav += self._generate_repeated_items(
                    link_names, group, no_of_repeats, is_current_group, current_group_instance)

        elif no_of_repeats > 0:
            target_location = self._get_location_for_section(section, groups)
            item = self._build_single_repeating_navigation(section, current_group_id, target_location)
            repeating_nav.append(item)

        return repeating_nav

    def _build_single_repeating_navigation(self, section, current_group_id, target_location):
        group_ids = (group['id'] for group in section['groups'])
        is_highlighted = current_group_id in group_ids
        is_completed = self.completeness.is_section_complete(section)
        return self._generate_item(section['title'], is_completed, target_location, is_highlighted)

    def _generate_repeated_items(self, link_names, group, no_of_repeats, is_current_group,
                                 current_group_instance):
        """
        Generates a lists of navigation items

        :param link_names: The list of titles to use for each link
        :param target_location: The target for the section link
        :param completed_id: The block_id which indicates whether this group has been completed
        :param no_of_repeats: The number of times to repeat
        :param is_current_group: Whether the repeated items are being generated for the current selected group
        :param current_group_instance: The current selected group_instance
        :return: A list of navigation items represented as dicts
        """

        nav_items = []

        for i in range(no_of_repeats):
            location = self._get_location_for_group(group, group_instance=i)
            is_current_group_instance = is_current_group and i == current_group_instance
            is_completed = self.completeness.is_group_complete(group, group_instance=i)

            nav_item = self._generate_item(
                name=link_names.get(i),
                completed=is_completed,
                location=location,
                highlight=is_current_group_instance,
                repeating=True,
            )
            nav_items.append(nav_item)

        return nav_items

    def _generate_item(self, name, completed, location, highlight, repeating=False):
        return {
            'link_name': name,
            'link_url': location.url(self.metadata),
            'completed': completed,
            'highlight': highlight,
            'repeating': repeating,
        }

    def _generate_link_names(self, label_answer_ids):
        link_names = defaultdict(list)

        for answer_id in label_answer_ids:
            for answer in self.answer_store.filter(answer_ids=[answer_id]).escaped():
                if answer['value']:
                    link_names[answer['answer_instance']].append(answer['value'])

        for link_name in link_names:
            link_names[link_name] = ' '.join(link_names[link_name])

        return link_names

    def _get_location_for_section(self, section, groups):
        section_completeness = self.completeness.get_state_for_section(section)
        first_incomplete = self.completeness.get_first_incomplete_location_in_section(section)
        first_group, last_group = groups[0], groups[-1]

        return self._get_location_for_completeness(
            section_completeness,
            first_group,
            last_group,
            first_group['blocks'][0],
            last_group['blocks'][-1],
            first_incomplete,
        )

    def _get_location_for_group(self, group, group_instance=None):
        """Gets the location for a link used for a repeating group
        """
        group_completeness = self.completeness.get_state_for_group(group, group_instance=group_instance)
        first_incomplete = self.completeness.get_first_incomplete_location_in_group(group, group_instance=group_instance)

        return self._get_location_for_completeness(
            group_completeness,
            group,
            group,
            group['blocks'][0],
            group['blocks'][-1],
            first_incomplete,
            group_instance=group_instance or 0,
        )

    @staticmethod
    def _get_location_for_completeness(
            completeness_state,
            first_group,
            last_group,
            first_block,
            last_block,
            first_incomplete,
            group_instance=0):
        if completeness_state == Completeness.STARTED:
            # if it's been started then get the first incomplete block within that section
            location = first_incomplete
        else:
            if completeness_state == Completeness.NOT_STARTED or last_block['type'] != 'SectionSummary':
                # if the section hasn't been started or it is complete but has no section summary
                # go to the first block
                target_group, target_block = first_group, first_block

            else:
                target_group, target_block = last_group, last_block

            location = Location(
                target_group['id'], group_instance, target_block['id'])

        return location
