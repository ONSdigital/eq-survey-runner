import copy
from collections import defaultdict

from structlog import get_logger

from app.helpers.schema_helper import SchemaHelper
from app.questionnaire.location import Location
from app.questionnaire.rules import evaluate_repeat, evaluate_skip_condition

logger = get_logger()


class Navigation(object):
    """
    Reads navigation config from the schema and returns collections of dicts that describe
    completion status of each group
    """
    def __init__(self, survey_json, answer_store, metadata=None, completed_blocks=None, routing_path=None):
        self.survey_json = survey_json
        self.metadata = metadata or {}
        self.answer_store = answer_store
        self.completed_blocks = completed_blocks or []
        self.routing_path = routing_path

    def build_navigation(self, current_group_id, current_group_instance):
        """
        Build navigation based on the current group/instance selected

        :param current_group_id:
        :param current_group_instance:
        :return:
        """
        if self.survey_json.get('navigation', False) is False:
            return None

        navigation = []

        last_group_id = SchemaHelper.get_last_group_id(self.survey_json)

        for group in filter(lambda x: 'hide_in_navigation' not in x, self.survey_json['groups']):
            logger.debug("building frontend navigation", group_id=group['id'])

            first_location = Location(group['id'], 0, group['blocks'][0]['id'])
            last_block_in_group = SchemaHelper.get_last_block_in_group(group)

            is_summary_or_confirm_group = last_block_in_group and \
                SchemaHelper.is_summary_or_confirmation(last_block_in_group)

            last_block_location = Location(group['id'], 0, last_block_in_group['id'])
            can_get_to_summary = is_summary_or_confirm_group and self.routing_path and \
                last_block_location in self.routing_path

            skip_group = self._should_skip_group(current_group_instance, group)
            if not skip_group:
                repeating_rule = SchemaHelper.get_repeat_rule(group)
                if repeating_rule:
                    logger.debug("building repeating navigation", group_id=group['id'])
                    navigation.extend(self._build_repeating_navigation(repeating_rule, group, current_group_id,
                                                                       current_group_instance))
                elif last_group_id == group['id'] and can_get_to_summary:
                    logger.debug("building navigation", group_id=group['id'])
                    if len(self.completed_blocks) > 0 and set(self.routing_path[:-1]).issubset(self.completed_blocks):
                        navigation.append(self._build_single_navigation(group, current_group_id, first_location))
                elif last_group_id != group['id'] and not is_summary_or_confirm_group:
                    logger.debug("building navigation", group_id=group['id'])
                    navigation.append(self._build_single_navigation(group, current_group_id, first_location))

        return navigation

    def _should_skip_group(self, current_group_instance, group):

        skip_group = False
        skip_condition = SchemaHelper.get_skip_condition(group)

        if skip_condition:
            skip_group = evaluate_skip_condition(skip_condition, self.metadata, self.answer_store,
                                                 current_group_instance)
        return skip_group

    def _build_repeating_navigation(self, repeating_rule, group, current_group_id, current_group_instance):
        first_location = Location(group['id'], 0, group['blocks'][0]['id'])
        no_of_repeats = evaluate_repeat(repeating_rule, self.answer_store)

        repeating_nav = []

        if repeating_rule['type'] == 'answer_count':
            completed_id = group['completed_id'] if 'completed_id' in group else group['blocks'][-1]['id']
            is_current_group = group['id'] == current_group_id
            link_names = self._generate_link_names(repeating_rule)

            repeating_nav = self._generate_repeated_items(link_names, first_location, completed_id, no_of_repeats,
                                                          is_current_group, current_group_instance)

        elif no_of_repeats > 0:
            item = self._build_single_navigation(group, current_group_id, first_location)
            repeating_nav.append(item)

        return repeating_nav

    def _build_single_navigation(self, group, current_group_id, first_location):
        completed_id = group['completed_id'] if 'completed_id' in group else group['blocks'][-1]['id']
        default_highlight = self._should_highlight(group, current_group_id)
        is_completed = self._is_complete_non_repeating(completed_id)

        return self._generate_item(group['title'], is_completed, first_location, default_highlight)

    @staticmethod
    def _should_highlight(group, current_group_id):
        is_current_group = group['id'] == current_group_id
        current_group_in_highlight = 'highlight_when' in group and current_group_id in group['highlight_when']

        return (current_group_in_highlight and not is_current_group) or is_current_group

    def _is_complete_non_repeating(self, completed_id):
        """
        Determines whether the non-repeating item can be marked as complete in navigation

        :param completed_id: The block_id which indicates whether this group has been completed
        :return:
        """
        for b in self.completed_blocks:
            if b.block_id == completed_id:
                return True
        return False

    def _is_complete_repeating(self, group_instance, completed_id):
        """
        Determines whether the repeating item can be marked as complete in navigation

        :param group_instance:
        :param completed_id: The block_id which indicates whether this group has been completed
        :return:
        """
        for b in self.completed_blocks:
            if b.group_instance == group_instance and b.block_id == completed_id:
                return True
        return False

    def _generate_repeated_items(self, link_names, first_location, completed_id, no_of_repeats, is_current_group,
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
                    completed=self._is_complete_repeating(i, completed_id),
                    location=location,
                    highlight=is_current_group_instance,
                    repeating=True,
                )
                nav_items.append(nav_item)

        return nav_items

    def _generate_item(self, name, completed, location, highlight, repeating=False):
        return {
            "link_name": name,
            "link_url": location.url(self.metadata),
            "completed": completed,
            "highlight": highlight,
            "repeating": repeating,
        }

    def _generate_link_names(self, repeating_rule):
        link_names = defaultdict(list)
        if 'navigation_label_answer_ids' in repeating_rule:
            label_answer_ids = repeating_rule['navigation_label_answer_ids']
        else:
            label_answer_ids = [repeating_rule['answer_id']]

        for answer_id in label_answer_ids:
            answers = self.answer_store.filter(answer_id=answer_id)
            for answer in answers:
                if answer['value']:
                    link_names[answer['answer_instance']].append(answer['value'])

        for link_name in link_names:
            link_names[link_name] = " ".join(link_names[link_name])

        return link_names
