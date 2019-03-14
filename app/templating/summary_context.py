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

    for group in itertools.chain.from_iterable(group_lists):
        summary_group = Group(group, path, answer_store, metadata, schema, schema_context).serialize()
        groups.append(summary_group)

    return groups
