import itertools
from flask import url_for
from app.questionnaire.path_finder import PathFinder
from app.templating.summary.group import Group


def build_summary_rendering_context(schema, schema_json, answer_store, metadata):
    """
    Build questionnaire summary context containing metadata and content from the answers of the questionnaire
    :param schema: schema of the current questionnaire
    :param answer_store: all of the answers to the questionnaire
    :param metadata: all of the metadata
    :return: questionnaire summary context
    """
    navigator = PathFinder(schema, answer_store, metadata)
    path = navigator.get_full_routing_path()
    groups = []

    group_lists = (
        section['groups']
        for section in schema_json['sections']
    )

    for group in itertools.chain.from_iterable(group_lists):
        if group['id'] in [location.group_id for location in path] \
                and schema.group_has_questions(group['id']):
            groups.extend([Group(group, path, answer_store, metadata, url_for)])

    return groups
