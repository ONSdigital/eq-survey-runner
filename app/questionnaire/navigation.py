import copy
from collections import defaultdict

from structlog import get_logger

from app.questionnaire.location import Location
from app.questionnaire.path_finder import PathFinder
from app.questionnaire.rules import evaluate_repeat, evaluate_skip_conditions

logger = get_logger()


class Navigation(object):
    """
    Reads navigation config from the schema and returns collections of dicts that describe
    completion status of each group
    """
    def __init__(self, schema, answer_store, metadata, completed_blocks, routing_path):
        self.schema = schema
        self.metadata = metadata
        self.answer_store = answer_store
        self.completed_blocks = completed_blocks
        self.routing_path = routing_path

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

        summary_or_confirmation_blocks = self.schema.get_summary_and_confirmation_blocks()

        navigation = []

        for section in self.schema.sections:
            non_skipped_groups = self._get_non_skipped_groups(section)
            if not non_skipped_groups:
                continue

            first_group_id = non_skipped_groups[0]
            first_block_id = self.schema.get_first_block_id_for_group(first_group_id)

            if first_block_id in summary_or_confirmation_blocks \
                    and self._can_reach_summary_confirmation(first_group_id, first_block_id) is False:
                continue

            repeating_rule = self.schema.get_repeat_rule(
                self.schema.get_group(first_group_id))
            if repeating_rule:
                navigation.extend(self._build_repeating_navigation(repeating_rule, section, current_group_id,
                                                                   current_group_instance))
            else:
                navigation.append(self._build_single_navigation(section, current_group_id,
                                                                Location(first_group_id, 0, first_block_id)))

        return navigation

    def _get_non_skipped_groups(self, section):
        return [
            group['id'] for group in self._get_visible_groups_for_section(section)
            if not self._should_skip_group(group)
        ]

    def _should_skip_group(self, group):
        skip_conditions = group.get('skip_conditions')

        if skip_conditions:
            return evaluate_skip_conditions(skip_conditions, self.metadata, self.answer_store)

        for block in reversed(group['blocks']):
            skip_conditions = block.get('skip_conditions')
            return evaluate_skip_conditions(skip_conditions, self.metadata, self.answer_store)

        return False

    def _can_reach_summary_confirmation(self, group_id, block_id):
        if self.routing_path and Location(group_id, 0, block_id) in self.routing_path and \
                self.completed_blocks and set(self.routing_path[:-1]).issubset(self.completed_blocks):
            return True

        return False

    def _build_single_navigation(self, section, current_group_id, first_location):
        group_ids = (group['id'] for group in self._get_visible_groups_for_section(section))
        is_highlighted = current_group_id in group_ids
        is_completed = self._is_completed(section)

        return self._generate_item(section['title'], is_completed, first_location, is_highlighted)

    def _build_repeating_navigation(self, repeating_rule, section, current_group_id, current_group_instance):
        first_group = next(self._get_visible_groups_for_section(section))
        first_location = Location(first_group['id'], 0, first_group['blocks'][0]['id'])
        answer_ids_on_path = PathFinder.get_answer_ids_on_routing_path(self.schema, self.routing_path)
        no_of_repeats = evaluate_repeat(repeating_rule, self.answer_store, answer_ids_on_path)

        repeating_nav = []

        if repeating_rule['type'] == 'answer_count':
            is_current_group = first_group['id'] == current_group_id
            link_names = self._generate_link_names(section['title_from_answers'])

            repeating_nav = self._generate_repeated_items(link_names, first_location, section, no_of_repeats,
                                                          is_current_group, current_group_instance)

        elif no_of_repeats > 0:
            item = self._build_single_repeating_navigation(section, current_group_id, first_location, no_of_repeats)
            repeating_nav.append(item)

        return repeating_nav

    def _build_single_repeating_navigation(self, section, current_group_id, first_location, no_of_repeats):
        group_ids = (group['id'] for group in self._get_visible_groups_for_section(section))
        is_highlighted = current_group_id in group_ids
        is_completed = self._is_completed_single_repeating(no_of_repeats, section)
        return self._generate_item(section['title'], is_completed, first_location, is_highlighted)

    def _is_completed_single_repeating(self, no_of_repeats, section):
        for i in range(no_of_repeats):
            if self._is_completed(section, i) is False:
                return False

        return True

    def _is_completed(self, section, group_instance=0):
        """
        Determines whether an item can be marked as complete in navigation

        :param completed_id: The block_id which indicates whether this group has been completed
        :param group_instance: Used for repeating groups
        :return:
        """
        contains_group_in_routing_path = False
        for group in section['groups']:
            group_id = group['id']
            for location in self.routing_path:
                if location.group_id == group_id and location.group_instance == group_instance:
                    contains_group_in_routing_path = True
                    if location not in self.completed_blocks:
                        return False

        return contains_group_in_routing_path

    def _generate_repeated_items(self, link_names, first_location, section, no_of_repeats, is_current_group,
                                 current_group_instance):
        """
        Generates a lists of navigation items

        :param link_names: The list of titles to use for each link
        :param first_location: The first group location
        :param completed_id: The block_id which indicates whether this group has been completed
        :param no_of_repeats: The number of times to repeat
        :param is_current_group: Whether the repeated items are being generated for the current selected group
        :param current_group_instance: The current selected group_instance
        :return: A list of navigation items represented as dicts
        """
        nav_items = []

        for i in range(no_of_repeats):
            location = copy.copy(first_location)
            location.group_instance = i
            is_current_group_instance = is_current_group and i == current_group_instance

            if link_names:
                nav_item = self._generate_item(
                    name=link_names.get(i),
                    completed=self._is_completed(section, i),
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

    @staticmethod
    def _get_visible_groups_for_section(section):
        return (
            group for group in section['groups']
            if not group.get('hide_in_navigation')
        )
