from flask import url_for

from app.questionnaire.path_finder import PathFinder
from app.templating.summary.section import Section


def build_summary_rendering_context(schema_json, answer_store, metadata):
    """
    Build questionnaire summary context containing metadata and content from the answers of the questionnaire
    :param schema_json: schema of the current questionnaire
    :param answer_store: all of the answers to the questionnaire
    :param metadata: all of the metadata
    :return: questionnaire summary context
    """
    navigator = PathFinder(schema_json, answer_store, metadata)
    path = navigator.get_routing_path()
    sections = []
    for group in schema_json['groups']:
        for block in group['blocks']:
            if block['id'] in [location.block_id for location in path] and block['type'] == 'Questionnaire':
                    link = url_for('questionnaire.get_block',
                                   eq_id=metadata['eq_id'],
                                   form_type=metadata['form_type'],
                                   collection_id=metadata['collection_exercise_sid'],
                                   group_id=group['id'],
                                   group_instance=0,
                                   block_id=block['id'])
                    sections.extend([Section(section, answer_store.map(), link) for section in block['sections']])
    return sections
