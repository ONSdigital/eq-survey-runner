import itertools

from app.questionnaire.path_finder import PathFinder
from app.templating.summary.group import Group


def build_summary_rendering_context(schema, sections, answer_store, metadata, schema_context):
    """
    Build questionnaire summary context containing metadata and content from the answers of the questionnaire
    :param schema: schema of the current questionnaire
    :param sections: the sections of the current schema
    :param answer_store: all of the answers to the questionnaire
    :param metadata: all of the metadata
    :param schema_context: The schema context
    :return: questionnaire summary context
    """
    navigator = PathFinder(schema, answer_store, metadata, [])
    path = navigator.get_full_routing_path()
    groups = []

    group_lists = (
        section['groups']
        for section in sections
    )

    group_ids_on_path = [location.group_id for location in path]

    for group in itertools.chain.from_iterable(group_lists):
        if (group['id'] in group_ids_on_path and schema.group_has_questions(group['id'])):
            no_of_repeats = _number_of_repeats(group, path)
            repeating_groups = []
            for instance_idx in range(0, no_of_repeats):
                summary_group = Group(group, path, answer_store, metadata, schema, instance_idx, schema_context).serialize()
                if summary_group['blocks']:
                    repeating_groups.extend([summary_group])
            groups.extend(repeating_groups)

    return groups


def _number_of_repeats(group, path):
    group_instances_on_path = [location.group_instance for location in path if location.group_id == group['id']]
    return len(set(group_instances_on_path))
